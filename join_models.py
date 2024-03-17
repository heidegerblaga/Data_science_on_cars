from regresion import X_train_scaled, X_test_scaled, y_test

import numpy as np
import tensorflow as tf
from sklearn.metrics import mean_squared_error

# Wczytanie modeli
model_bmw = tf.keras.models.load_model('bmw.h5')
model_audi = tf.keras.models.load_model('audi.h5')

# Warstwa klasyfikująca na podstawie marki samochodu
classification_layer = tf.keras.layers.Dense(2, activation='softmax')

# Warstwa wejściowa
input_layer = tf.keras.layers.Input(shape=(X_train_scaled.shape[1],))

# Warstwa klasyfikacji
classification_output = classification_layer(input_layer)

# Wyjścia z modeli BMW i Audi
output_bmw = model_bmw(input_layer)
output_audi = model_audi(input_layer)


# Przekierowanie do odpowiedniego modelu na podstawie klasyfikacji
final_output = tf.keras.layers.Add()([
    tf.keras.layers.Multiply()([output_bmw, classification_output]),
    tf.keras.layers.Multiply()([output_audi, classification_output])
])

# Tworzenie ostatecznego modelu
final_model = tf.keras.models.Model(inputs=input_layer, outputs=final_output)

# Ocena modelu na zbiorze testowym
y_pred = final_model.predict(X_test_scaled)
mse = mean_squared_error(y_test, y_pred)
print('Mean Squared Error on Test Data:', mse)

# Przewidywanie wartości za pomocą ostatecznego modelu
new_data = np.array([[320000, 2006, 231, 2993, 11, 4, 65, 2, 336, 1, 9, 483, 3, 2, 3, 2, 3, 1]])
predykcje = final_model.predict(new_data)

print("Przewidywane ceny dla nowych danych:")
print(predykcje)

# Zapisanie ostatecznego modelu do pliku h5
final_model.save('final_model.h5')

print("Ostateczny model został zapisany.")

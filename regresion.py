import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from keras.models import Sequential
from keras.layers import Dense, Dropout
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
scaler = StandardScaler()


# Wczytanie danych
cars = pd.read_pickle('cars.pickle')  # Zastąp 'dane.csv' nazwą swojego pliku danych
cars = cars[cars['marka']==65]


target = cars['cena']
features = cars.drop({'cena','id'}, axis=1)

# Podział danych na zbiór treningowy i testowy
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

# Standaryzacja danych
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)


model = Sequential()
model.add(Dense(16, activation='relu', name='my_dense_layr', input_shape=(X_train_scaled.shape[1],)))
model.add(Dense(32, name='my_dense_layr1', activation='relu'))
model.add(Dense(1, name='my_dense_layr2'))  # Warstwa wyjściowa dla regresji

model.compile(optimizer='adam', loss='mean_squared_error')

# Trenowanie modelu
model.fit(X_train, y_train, epochs=1000)


model.save('bmw.h5')

#model = tf.keras.models.load_model('audi.h5')

# Ocena modelu na zbiorze testowym
y_pred = model.predict(X_test_scaled)
mse = mean_squared_error(y_test, y_pred)
print('Mean Squared Error on Test Data:', mse)


# Przewidywanie wartości za pomocą wczytanego modelu
predykcje = model.predict(np.array([[17500, 2022, 231, 2967, 8, 5, 15, 1, 321, 2, 9, 111, 2, 4, 3, 1, 3, 1]]))

print("Przewidywane ceny dla nowych danych:")
print(predykcje)
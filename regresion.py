import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()


# Wczytanie danych
cars = pd.read_pickle('cars.pickle')  # Zastąp 'dane.csv' nazwą swojego pliku danych
cars = cars[cars['marka']==65]
cars['przebieg'] = scaler.fit_transform(cars[['przebieg']])
cars['cena'] = scaler.fit_transform(cars[['cena']])


target = cars['cena']
features = cars.drop({'cena','id'}, axis=1)

# Podział danych na zbiór treningowy i testowy
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

# Standaryzacja danych
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Budowa modelu
model = Sequential()
model.add(Dense(64, activation='relu', input_shape=(X_train_scaled.shape[1],)))
model.add(Dropout(0.2))  # Dropout dla regularyzacji
model.add(Dense(32, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(1))  # Warstwa wyjściowa dla regresji

model.compile(optimizer='adam', loss='mean_squared_error')

# Trenowanie modelu
model.fit(X_train_scaled, y_train, epochs=1000, batch_size=32, validation_split=0.2, verbose=1)

# Ocena modelu na zbiorze testowym
y_pred = model.predict(X_test_scaled)
mse = mean_squared_error(y_test, y_pred)
print('Mean Squared Error on Test Data:', mse)

nowe_dane = np.array([[1.471000, 2006, 2993, 231, 11, 4, 65, 2, 336, 1, 9, 483, 3, 2, 3, 2, 3, 1]])

# Przewidywanie wartości za pomocą wczytanego modelu
predykcje = model.predict(np.array([[1.471000, 2006, 2993, 231, 11, 4, 65, 2, 336, 1, 9, 483, 3, 2, 3, 2, 3, 1]])
)

print("Przewidywane ceny dla nowych danych:")
print(predykcje)

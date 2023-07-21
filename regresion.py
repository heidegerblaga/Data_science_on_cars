import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import pickle

# Odczytanie DataFrame z pliku pickle
nazwa_pliku = 'cars.pickle'
cars = pd.read_pickle(nazwa_pliku)

# Przygotowanie danych treningowych z DataFrame
X = cars[['id_generacja', 'id_kolor', 'id_kraj', 'id_marki', 'id_nadwozia', 'id_naped',
          'id_paliwo', 'id_pierwszy_wlasciciel', 'id_polska', 'id_skrzynia', 'id_stan']].values
Y = cars['cena'].values

# Tworzenie modelu sieci neuronowej
model = Sequential()
model.add(Dense(16, activation='relu', input_shape=(11,)))
model.add(Dense(8, activation='relu'))
model.add(Dense(1))

# Kompilacja modelu
model.compile(optimizer='adam', loss='mse')

# Trenowanie modelu (zakładam, że masz dane do trenowania, w tym przypadku pomijam trenowanie)
# model.fit(X, Y, epochs=10, batch_size=1)

nazwa_pliku_modelu = 'model.pickle'

# Zapisanie modelu do pliku pickle
with open(nazwa_pliku_modelu, 'wb') as plik:
    pickle.dump(model, plik)

# Odczytanie modelu z pliku pickle
with open(nazwa_pliku_modelu, 'rb') as plik:
    wczytany_model = pickle.load(plik)

# Przygotowanie danych do przewidywania - zamień słownik na tablicę numpy
nowe_dane = np.array([[388, 10, 18, 3, 2, 6, 3, 2, 1, 2, 1]])

# Przewidywanie wartości za pomocą wczytanego modelu
predykcje = wczytany_model.predict(nowe_dane)

print("Przewidywane ceny dla nowych danych:")
print(predykcje)

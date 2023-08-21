import statsmodels.api as sm
import pandas as pd

cars = pd.read_pickle('cars.pickle')

X = sm.add_constant(cars['marka'])

# Tworzenie modelu regresji liniowej
model = sm.OLS(cars['cena'], X).fit()

# Wypisanie wyników
print(model.summary())
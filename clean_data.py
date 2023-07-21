import pandas as pd
import psycopg2


conn = psycopg2.connect(user="postgres",
              password="qwest1",
              host="localhost",
              database="otomoto")


query = "SELECT * FROM numcars"

cars = pd.read_sql(query,conn)
kolumny_do_zamiany = ['cena']
cars['cena'] = cars['cena'].str.replace('EUR', '').str.replace(' ', '').str.replace(',', '.').astype(float)

cars['rok_produkcji'] = cars['rok_produkcji'].astype(float)

cars['moc'] = cars['moc'].str.replace(' KM', '').str.replace(' ', '0').astype(float)


cars['pojemnosc'] = cars['pojemnosc'].str.replace('cm3', '').str.replace(' ', '').str.replace('', '0').astype(float)

cars['spalanie'] = cars['spalanie'].str.replace('l/100km',' ').str.replace(' ', '0').str.replace(',', '.').astype(float)

cars['liczba_drzwi'] = cars['liczba_drzwi'].str.replace(' ', '0').astype(float)

cars['liczba_miejsc'] = cars['liczba_miejsc'].str.replace(' ', '0').astype(float)

print(cars.loc[1])

nazwa_pliku = 'cars.pickle'

cars.to_pickle(nazwa_pliku)














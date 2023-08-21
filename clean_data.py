import pandas as pd
import psycopg2


conn = psycopg2.connect(user="postgres",
              password="qwest1",
              host="localhost",
              database="otomoto")


query = "SELECT * FROM numcars"

cars = pd.read_sql(query,conn)


cars['cena'] = cars['cena'].str.replace('EUR', '').str.replace(' ', '').str.replace(',', '.').astype(float) #kurs euro

cars['rok_produkcji'] = cars['rok_produkcji'].astype(float)

cars['moc'] = cars['moc'].str.replace(' KM', '').str.replace(' ', '0').astype(float)


cars['pojemnosc'] = cars['pojemnosc'].str.replace('cm3', '').str.replace(' ', '').str.strip()


cars['spalanie'] = cars['spalanie'].str.replace('l/100km','').str.replace(',','.').str.strip()

cars['liczba_drzwi'] = cars['liczba_drzwi'].str.replace(' ', '0').astype(float)

cars['przebieg'] = cars['przebieg'].str.replace(' km','').str.replace(' ', '')

cars = cars.applymap(lambda x: 0 if x == '' else x)

cars['spalanie'] = cars['spalanie'].astype(float)

cars['pojemnosc'] = cars['pojemnosc'].astype(float)

cars['przebieg'] = cars['przebieg'].astype(float)



cars = cars[(cars != 0).all(axis=1)].reset_index(drop=True)


print(cars)


nazwa_pliku = 'cars.pickle'

cars.to_pickle(nazwa_pliku)














from bs4 import BeautifulSoup
from requests import get
import re
from models import (Base, session, Cars, engine)
import multiprocessing

import pandas as pd





faster = ["https://www.otomoto.pl/osobowe?page="+str(page)+"&search%5Badvanced_search_expanded%5D=true" for page in range(2,6000)]

# Dodawanie do bazy danych informacji z konkretnego ogłoszenia
def det(link):


    page = get(link)
    bs = BeautifulSoup(page.content, 'html.parser')
    marka = bs.find_all(class_="ooa-162vy3d e18eslyg3")

    mymap = {"Oferta od": " ", "Marka pojazdu": " ", "Model pojazdu": " ",
             "Typ nadwozia": " ", "Generacja": " ", "Kolor": " ", "Rodzaj koloru": " ",
             "Rok produkcji": "", "Przebieg": "", "Pojemność skokowa": "",
             "Rodzaj paliwa": " ", "Moc": " ", "Skrzynia biegów": " ",
             "Napęd": " ", "Liczba drzwi": " ", "Liczba miejsc": " ",
             "Kraj pochodzenia": " ", "Data pierwszej rejestracji w historii pojazdu": " ",
             "Zarejestrowany w Polsce": " ", "Pierwszy właściciel (od nowości)": " ", "Bezwypadkowy": " ",
             "Serwisowany w ASO": " ", "Stan": " ", "Numer rejestracyjny pojazdu": " ",
             "Spalanie W Mieście": " ", "Spalanie Poza Miastem": " ", "Wersja": " ", "Emisja": " ",
             "Okres gwarancji producenta": " ", "Pokaż oferty z numerem VIN": " ", "Możliwość finansowania": " ",
             "Leasing": " "}

    for info in marka:


        for key in mymap:

            if bool(re.search(f"{key}", info.get_text())):
                new = re.sub(f"{key}", r"", info.get_text())
                mymap[key] = new

    print(mymap)





    ID = bs.find(class_="ooa-1neiy54 edazosu6").get_text()[3:].strip()



    car = Cars(oferta_od=mymap["Oferta od"],marka_pojazdu =mymap["Marka pojazdu"],model_pojazdu = mymap["Model pojazdu"],
                        typ_nadwozia = mymap["Typ nadwozia"],generacja = mymap["Generacja"],rodzaj_paliwa=mymap["Rodzaj paliwa"],
                        przebieg=mymap["Przebieg"],rok_produkcji=mymap["Rok produkcji"],numer_rej=mymap["Numer rejestracyjny pojazdu"],
                        pojemnosc=mymap["Pojemność skokowa"],moc=mymap["Moc"],skrzyniabieg=mymap["Skrzynia biegów"],
                        naped=mymap["Napęd"],spalanie=mymap["Spalanie W Mieście"],liczba_drzwi=mymap["Liczba drzwi"],
                        zarejestrowany_w_pol=mymap["Zarejestrowany w Polsce"],liczba_miejsc=mymap["Liczba miejsc"],
                        kolor=mymap["Kolor"],kraj=mymap["Kraj pochodzenia"],pierwsza_rej=mymap["Data pierwszej rejestracji w historii pojazdu"],
                        stan=mymap["Stan"],bezwypadkowy=mymap["Bezwypadkowy"],pierwszy_wlasciciel=mymap["Pierwszy właściciel (od nowości)"]
                        ,cena=bs.find(class_="ooa-1xhj18k eqdspoq2").get_text().split('PLN')[0].strip(),id=ID
                        )

    session.add(car)

    try:
          session.commit()

    except Exception as e:
          print(e)



# pobieranie listy ofert i przejscie do kolejnej strony po ich zaladowaniu
def offerlist(url):

    page = get(url)
    bs = BeautifulSoup(page.content, 'html.parser')



    # link do oferty
    linki = re.findall(r'https://www.otomoto.pl/[-\w\d/.]+', str(bs.findAll(target="_self")))


    i = 0
    for link in linki:
        det(link)

    print(url)

    if url == "https://www.otomoto.pl/osobowe":

        url = "https://www.otomoto.pl/osobowe?page=2"

    else:

        print(url)
        page = str(int(re.findall(r'\d+', str(re.findall(r'page=\d+', url)))[0]) + 1)

        url = "https://www.otomoto.pl/osobowe?page=" + page

    offerlist(url)


if __name__=='__main__':

    page = get("https://www.otomoto.pl/osobowe")

    bs = BeautifulSoup(page.content, 'html.parser')



    offerlist("https://www.otomoto.pl/osobowe")





   # id ogloszenia











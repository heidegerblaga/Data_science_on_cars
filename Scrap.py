from bs4 import BeautifulSoup
from requests import get
import re
from models import (Base, session, Cars, engine)
import multiprocessing
import pandas as pd



# TODO : Wielowątkowość

faster = ["https://www.otomoto.pl/osobowe?page="+str(page)+"&search%5Badvanced_search_expanded%5D=true" for page in range(2,6000)]

# Dodawanie do bazy danych informacji z konkretnego ogłoszenia
def det(link,ID):


             #existing_record = session.query(Cars).filter_by(id=id).first()
        try:
             mymap = {"Oferta od": " ", "Marka pojazdu": " ", "Model pojazdu": " ",
                      "Typ nadwozia": " ", "Generacja": " ", "Kolor": " ", "Rodzaj koloru": " ",
                      "Rok produkcji": "", "Przebieg": "", "Pojemność skokowa": "",
                      "Rodzaj paliwa": " ", "Moc": " ", "Skrzynia biegów": " ",
                      "Napęd": " ", "Liczba drzwi": " ", "Liczba miejsc": " ",
                      "Kraj pochodzenia": " ", "Data pierwszej rejestracji w historii pojazdu": " ",
                      "Zarejestrowany w Polsce": " ", "Pierwszy właściciel (od nowości)": " ", "Bezwypadkowy": " ",
                      "Serwisowany w ASO": " ", "Stan": " ", "Numer rejestracyjny pojazdu": " ",
                      "Spalanie W Mieście": " ", "Spalanie Poza Miastem": " ", "Wersja": " ", "Emisja": " ",
                      "Okres gwarancji producenta": " ", "Pokaż oferty z numerem VIN": " ",
                      "Możliwość finansowania": " ",
                      "Leasing": " "}

             df = pd.DataFrame(columns=["Oferta od", "Marka pojazdu", "Model pojazdu",
                      "Typ nadwozia", "Generacja", "Kolor" "Rodzaj koloru",
                      "Rok produkcji", "Przebieg", "Pojemność skokowa"
                      "Rodzaj paliwa", "Moc", "Skrzynia biegów",
                      "Napęd", "Liczba drzwi", "Liczba miejsc",
                      "Kraj pochodzenia", "Data pierwszej rejestracji w historii pojazdu",
                      "Zarejestrowany w Polsce", "Pierwszy właściciel (od nowości)", "Bezwypadkowy",
                      "Serwisowany w ASO", "Stan", "Numer rejestracyjny pojazdu",
                      "Spalanie W Mieście", "Spalanie Poza Miastem" , "Wersja", "Emisja",
                      "Okres gwarancji producenta", "Pokaż oferty z numerem VIN",
                      "Możliwość finansowania",
                      "Leasing"])

             page = get(link)

             details = BeautifulSoup(page.content, 'html.parser')

             offer = details.find(class_="ooa-w4tajz e18eslyg0")

             # print(offer.get_text())
             for key in mymap.keys():
                 # Utwórz wzorzec regex, który szuka klucza i wszystkiego po nim do następnego dużego klucza (rozpoczynającego się od wielkiej litery)


                 pattern = f"{key}(.*?)(?=(?:{'|'.join(map(re.escape, mymap.keys()))}|$))"
                 match = re.search(pattern, offer.get_text().replace("Kup ten pojazd na ratyObliczVINWyświetl VIN", "")
                                   .replace("Pokaż oferty z numerem VINTakMa numer rejestracyjnyTak", "")
                                   .replace(
                     "14 pól zweryfikowanychSzczegółowe dane pojazdu zostały zweryfikowane poprzez porównanie ich z rządową bazą danych",
                     ""))
                 if match:
                     mymap[key] = match.group(1).strip()

             info = re.sub(r"(\B[A-Z])", r" \1", offer.get_text())

             for i in range(0, len(info) - 1, 2):
                 mymap[info[i]] = info[i + 1]
             new_row_df = pd.DataFrame([mymap])

             # TODO : Nie dodawaj nowych kluczy

             # Dodawanie nowego wiersza do istniejącego DataFrame za pomocą concat
             df = pd.concat([df, new_row_df], ignore_index=True)
             print(df)
        except:
            pass

# car = Cars(oferta_od=mymap["Oferta od"],marka_pojazdu =mymap["Marka pojazdu"],model_pojazdu = mymap["Model pojazdu"],
         #            typ_nadwozia = mymap["Typ nadwozia"],generacja = mymap["Generacja"],rodzaj_paliwa=mymap["Rodzaj paliwa"],
         #            przebieg=mymap["Przebieg"],rok_produkcji=mymap["Rok produkcji"],numer_rej=mymap["Numer rejestracyjny pojazdu"],
         #            pojemnosc=mymap["Pojemność skokowa"],moc=mymap["Moc"],skrzyniabieg=mymap["Skrzynia biegów"],
         #            naped=mymap["Napęd"],spalanie=mymap["Spalanie W Mieście"],liczba_drzwi=mymap["Liczba drzwi"],
         #            zarejestrowany_w_pol=mymap["Zarejestrowany w Polsce"],liczba_miejsc=mymap["Liczba miejsc"],
         #            kolor=mymap["Kolor"],kraj=mymap["Kraj pochodzenia"],pierwsza_rej=mymap["Data pierwszej rejestracji w historii pojazdu"],
         #            stan=mymap["Stan"],bezwypadkowy=mymap["Bezwypadkowy"],pierwszy_wlasciciel=mymap["Pierwszy właściciel (od nowości)"]
         #            ,cena=details.find(class_="offer-price__number").get_text().split('PLN')[0].strip(),id=ID
         #            )
         #
         # session.add(car)

         # try:
         #  session.commit()
         # except:
         #     print("cos nie tak")



# pobieranie listy ofert i przejscie do kolejnej strony po ich zaladowaniu
def offerlist(url):

     page = get(url)
     bs = BeautifulSoup(page.content, 'html.parser')

     # id ogloszenia

     ID = list(map(lambda x: x.split("data-id=")[1].split("\"")[1], re.findall(r'data-id=["\d]+', str(bs.findAll(class_="ooa-yca59n e1oqyyyi0")))))




     # link do oferty
     linki = re.findall(r'https://www.otomoto.pl/[-\w\d/.]+', str(bs.findAll(target="_self")))

     print(url)
     for link in linki:

        det(link,ID)

     if url == "https://www.otomoto.pl/osobowe" :

          url = "https://www.otomoto.pl/osobowe?page=2"

     else :

          print(url)
          page = str(int(re.findall(r'\d+', str(re.findall(r'page=\d+', url)))[0]) + 1)

          url = "https://www.otomoto.pl/osobowe?page="+page



     offerlist(url)


if __name__=='__main__':

   page = get("https://www.otomoto.pl/osobowe")

   bs = BeautifulSoup(page.content, 'html.parser')

   ID = re.findall(r'data-id=["\d]+', str(bs.findAll(class_="ooa-yca59n e1oqyyyi0")))

   print(f"HALO {ID}")

   offerlist("https://www.otomoto.pl/osobowe")





   # id ogloszenia











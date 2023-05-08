from bs4 import BeautifulSoup
from requests import get
import re
from models import (Base, session, Cars, engine)
import multiprocessing





faster = ["https://www.otomoto.pl/osobowe?page="+str(page)+"&search%5Badvanced_search_expanded%5D=true" for page in range(2,6000) ]

def det(link,ID):

     existing_record = session.query(Cars).filter_by(id=ID).first()

     if existing_record is None:
         mymap = {"Oferta od": " ", "Marka pojazdu": " ", "Model pojazdu": " ",
                  "Typ nadwozia": " ", "Generacja": " ", "Kolor": " ",
                  "Rok produkcji": "", "Przebieg": "", "Pojemność skokowa": "",
                  "Rodzaj paliwa": " ", "Moc": " ", "Skrzynia biegów": " ",
                  "Napęd": " ", "Liczba drzwi": " ", "Liczba miejsc": " ",
                  "Kraj pochodzenia": " ", "Data pierwszej rejestracji w historii pojazdu": " ",
                  "Zarejestrowany w Polsce": " ", "Pierwszy właściciel (od nowości)": " ", "Bezwypadkowy": " ",
                  "Serwisowany w ASO": " ", "Stan": " ","Numer rejestracyjny pojazdu":" ",
                  "Spalanie W Mieście":" "}


         page = get(link)
         details = BeautifulSoup(page.content, 'html.parser')


         offer = details.find(class_="offer-params with-vin")





         info = list(map(lambda x : x.strip(),list(filter(lambda x: x!=''  ,offer.get_text().split('\n')))))


         for i in range(0,len(info)-1,2):

             mymap[info[i]]=info[i+1]

         print(mymap)


         car = Cars(oferta_od=mymap["Oferta od"],marka_pojazdu =mymap["Marka pojazdu"],model_pojazdu = mymap["Model pojazdu"],
                    typ_nadwozia = mymap["Typ nadwozia"],generacja = mymap["Generacja"],rodzaj_paliwa=mymap["Rodzaj paliwa"],
                    przebieg=mymap["Przebieg"],rok_produkcji=mymap["Rok produkcji"],numer_rej=mymap["Numer rejestracyjny pojazdu"],
                    pojemnosc=mymap["Pojemność skokowa"],moc=mymap["Moc"],skrzyniabieg=mymap["Skrzynia biegów"],
                    naped=mymap["Napęd"],spalanie=mymap["Spalanie W Mieście"],liczba_drzwi=mymap["Liczba drzwi"],
                    zarejestrowany_w_pol=mymap["Zarejestrowany w Polsce"],liczba_miejsc=mymap["Liczba miejsc"],
                    kolor=mymap["Kolor"],kraj=mymap["Kraj pochodzenia"],pierwsza_rej=mymap["Data pierwszej rejestracji w historii pojazdu"],
                    stan=mymap["Stan"],bezwypadkowy=mymap["Bezwypadkowy"],pierwszy_wlasciciel=mymap["Pierwszy właściciel (od nowości)"]
                    ,cena=details.find(class_="offer-price__number").get_text().split('PLN')[0].strip(),id=ID
                    )

         session.add(car)

         try:
          session.commit()
         except:
             print("cos nie tak")




def offerlist(url):

     page = get(url)
     bs = BeautifulSoup(page.content, 'html.parser')

     # id ogloszenia

     ID = list(map(lambda x: int(x.split("data-id=")[1].split("\"")[1]), re.findall(r'data-id=["\w]+', str(bs.findAll(class_="ooa-dmrg7i evg565y0")))))

     # link do oferty
     linki = re.findall(r'https://www.otomoto.pl/[-\w\d/.]+', str(bs.findAll(target="_self")))


     with multiprocessing.Pool() as pool:

            try:

             wyniki = pool.starmap(det, zip(linki,ID))

            except:
              pass





     if url == "https://www.otomoto.pl/osobowe" :

          url = "https://www.otomoto.pl/osobowe?page=2&search%5Badvanced_search_expanded%5D=true"

     else :

          print(url)
          page = str(int(re.findall(r'\d+', str(re.findall(r'page=\d+', url)))[0]) + 1)

          url = "https://www.otomoto.pl/osobowe?page="+page+"&search%5Badvanced_search_expanded%5D=true"



     offerlist(url)


if __name__=='__main__':


    offerlist("https://www.otomoto.pl/osobowe")
   #
   # page = get("https://www.otomoto.pl/osobowe")
   # bs = BeautifulSoup(page.content, 'html.parser')
   #
   # # id ogloszenia
   # ID = re.findall(r'data-id=["\w]+', str(bs.findAll(class_="ooa-dmrg7i evg565y0")))
   #
   # print(list(map(lambda x: x.split("data-id=")[1].split("\"")[1],ID)))








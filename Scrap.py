from bs4 import BeautifulSoup
from requests import get
import re
from models import (Base, session, Cars, engine)
import multiprocessing




def det(link):

     mymap = {}


     page = get(link)
     details = BeautifulSoup(page.content, 'html.parser')


     offer = details.find(class_="offer-params with-vin")

     info = list(map(lambda x : x.strip(),list(filter(lambda x: x!=''  ,offer.get_text().split('\n')))))
     #print(info)


     for i in range(0,len(info)-1,2):
          mymap[info[i]]=info[i+1]

     print(mymap)

     car = Cars(oferta_od=mymap["Oferta od"],marka_pojazdu = mymap["Marka pojazdu"],model_pojazdu = mymap["Model pojazdu"],typ_nadwozia = mymap["Typ nadwozia"],generacja = mymap["Generacja"])

     session.add(car)
     session.commit()

     #id = Column(Integer, primary_key=True)
     #cena = Column(String)

     # bool_numer_rej = Column(String)
     # numer_rej = Column(String)
     # pojemnosc = Column(String)
     # moc = Column(String)
     # skrzyniabieg = Column(String)
     # naped = Column(String)
     # spalanie = Column(String)
     # liczba_drzwi = Column(String)
     # liczba_miejsc = Column(String)
     # kolor = Column(String)
     # kraj = Column(String)
     # pierwsza_rej = Column(String)
     # liczba_drzwi = Column(String)
     # zarejstrowany_w_pol = Column(String)
     # stan = Column(String)
     # status = Column(String)






def offerlist(url):
     page = get(url)
     bs = BeautifulSoup(page.content, 'html.parser')

     # id ogloszenia
     print(re.findall(r'data-id=["\w]+', str(bs.findAll(class_="ooa-dmrg7i evg565y0"))))

     # link do oferty
     linki = re.findall(r'https://www.otomoto.pl/[-\w\d/.]+', str(bs.findAll(target="_self")))

     print(linki)

     with multiprocessing.Pool() as pool:

          try:
               wyniki = pool.map(det, linki)

          except:
               pass

     if url == "https://www.otomoto.pl/osobowe" :

          url = "https://www.otomoto.pl/osobowe?page=2&search%5Badvanced_search_expanded%5D=true"

     else :

          print(url)
          page = str(int(re.findall(r'\d+', str(re.findall(r'page=\d', url)))[0]) + 1)

          url = "https://www.otomoto.pl/osobowe?page="+page+"&search%5Badvanced_search_expanded%5D=true"


     offerlist(url)


if __name__=='__main__':

     url = "https://www.otomoto.pl/osobowe"

     linki = offerlist(url)





from sqlalchemy import Integer,String,Boolean,Column,Date,ForeignKey
from psql import engine
from sqlalchemy.orm import sessionmaker,relationship
from sqlalchemy.ext.declarative import declarative_base



Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

dbConnection = engine.connect()

# Read data from PostgreSQL database table and load into a DataFrame instance



class Cars(Base):

    __tablename__="cars"

    id = Column(Integer, primary_key=True)
    cena = Column(String)
    oferta_od = Column(String)
    marka_pojazdu = Column(String)
    model_pojazdu = Column(String)
    typ_nadwozia = Column(String)
    generacja = Column(String)
    rodzaj_paliwa = Column(String)
    przebieg = Column(String)
    rok_produkcji = Column(String)
    vin = Column(String)
    numer_rej = Column(String)
    pojemnosc = Column(String)
    moc = Column(String)
    skrzyniabieg = Column(String)
    naped = Column(String)
    spalanie = Column(String)
    liczba_drzwi = Column(String)
    liczba_miejsc = Column(String)
    kolor = Column(String)
    kraj = Column(String)
    pierwsza_rej = Column(String)
    liczba_drzwi = Column(String)
    zarejstrowany_w_pol = Column(String)
    stan = Column(String)
    status = Column(String)
    # musisz jeszcze pododawać rzeczy ze statusu pojazdu








if __name__ == '__main__':
    Base.metadata.create_all(engine)
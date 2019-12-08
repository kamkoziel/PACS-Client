import random
import string
from bitmap import BitMap

import gdcm
import os
from numpy.core import byte

import app.DPCModel.DatabaseModel  as db
import pydicom as dc


class PACS_Action():
    @staticmethod
    def isConnect():
        user = db.get_active_user()
        archive = db.get_active_archive()
        response = gdcm.CompositeNetworkFunctions.CEcho(user[2], int(archive[3]), user[1], archive[1])
        return response

    @staticmethod
    def storeDICOM(pathToItem):
        klient = db.get_active_user()
        archive = db.get_active_archive()
        #print(int(klient[3]))
        file = gdcm.FilenamesType()
        file.append(pathToItem)
        print(klient[3])
        response = gdcm.CompositeNetworkFunctions.CStore(str(klient[2]), int(archive[3]), file, str(klient[1]), str(archive[1]))
        return response

    @staticmethod
    def findPatients():
        klient = db.get_active_user()
        archive = db.get_active_archive()

        # klucze(filtrowanie lub określenie, które dane są potrzebne)
        klucze = gdcm.KeyValuePairArrayType()

        tag = gdcm.Tag(0x0010, 0x0010)  # 10, 10 == PATIENT_NAME
        klucz1 = gdcm.KeyValuePairType(tag, "*")  # * == dowolne imię
        klucze.append(klucz1)
        klucze.append(gdcm.KeyValuePairType(gdcm.Tag(0x0010, 0x0020), ""))
        print('Keys - READY! \n Makeing query....')
        # zwrotnie oczekujemy wypełnionego 10, 20 czyli PATIENT_ID

        # skonstruuj zapytanie gdcm.BaseRootQuery
        zapytanie = gdcm.CompositeNetworkFunctions.ConstructQuery(gdcm.ePatientRootType, gdcm.ePatient, klucze)
        print('Query - READY! \n Finding....')
        # sprawdź, czy zapytanie spełnia kryteria
        if not zapytanie.ValidateQuery():
            print("FIND błędne zapytanie!")
            return

        # kontener na wyniki
        wynik = gdcm.DataSetArrayType()

        # wykonaj zapytanie
        stan = gdcm.CompositeNetworkFunctions.CFind(str(klient[2]), int(archive[3]), zapytanie, wynik, str(klient[1]),
                                                    str(archive[1]))
        print('Finding - READY!')
        print(wynik)
        # sprawdź stan
        if (not stan):
            print("Program isn't able to find any patients")
            return None
        print("All patients are found")
        response = []
        print(wynik)
        # pokaż wyniki
        for x in wynik:
            print(str(x))  # cała odpowiedź jako wielolinijkowy napis
            response.append([str(x.GetDataElement(gdcm.Tag(0x0010, 0x0020)).GetValue()),
                             str(x.GetDataElement(gdcm.Tag(0x0010, 0x0010)).GetValue())])
        return response

    @staticmethod
    def find_patients(patientID: str = None):
        print('Getting actie archive and user...')
        klient = db.get_active_user()
        archive = db.get_active_archive()
        # klucze(filtrowanie lub określenie, które dane są potrzebne)
        klucze = gdcm.KeyValuePairArrayType()
        tag = gdcm.Tag(0x0010, 0x0010)  # 10, 10 == PATIENT_NAME
        if patientID is None:
            p_id_key = gdcm.KeyValuePairType(tag, "*") # * == dowolne imię
        else:
            p_id_key = gdcm.KeyValuePairType(tag, patientID)  # * == dowolne imię

        p_name_kay = gdcm.KeyValuePairType(gdcm.Tag(0x0010,0x0020), "")
        p_birth_key = gdcm.KeyValuePairType(gdcm.Tag(0x0010,0x0030),"")
        study_id = gdcm.KeyValuePairType(gdcm.Tag(0x0020, 0x0010), "")


        klucze.append(p_id_key)
        klucze.append(p_name_kay)
        #klucze.append(gdcm.KeyValuePairType(gdcm.Tag(0x0010, 0x0020), ""))
        print('Keys - READY! \n Makeing query....')
        # zwrotnie oczekujemy wypełnionego 10, 20 czyli PATIENT_ID

        # skonstruuj zapytanie gdcm.BaseRootQuery
        zapytanie = gdcm.CompositeNetworkFunctions.ConstructQuery(gdcm.ePatientRootType, gdcm.ePatient, klucze)
        print('Query - READY! \n Finding....')
        # sprawdź, czy zapytanie spełnia kryteria
        if not zapytanie.ValidateQuery() :
            print("FIND błędne zapytanie!")
            return []

        # kontener na wyniki
        wynik = gdcm.DataSetArrayType()

        # wykonaj zapytanie
        stan = gdcm.CompositeNetworkFunctions.CFind(str(klient[2]), int(archive[3]), zapytanie, wynik, str(klient[1]), str(archive[1]))

        # sprawdź stan
        if (not stan):
            print("Program isn't able to find any patients")
            return []
        if patientID is None:
            print("All patients are found")
        else:
            print("{} patient is found".format(patientID))
        response = []

        # pokaż wyniki
        for x in wynik:
            response.append([str(x.GetDataElement(gdcm.Tag(0x0010, 0x0020)).GetValue()),
                             str(x.GetDataElement(gdcm.Tag(0x0010, 0x0010)).GetValue())])
        return response

    @staticmethod
    def find_study(patientID: str = None):
        klient = db.get_active_user()
        archive = db.get_active_archive()
        # klucze(filtrowanie lub określenie, które dane są potrzebne)
        klucze = gdcm.KeyValuePairArrayType()

        if patientID is None:
            id_key = gdcm.KeyValuePairType(gdcm.Tag(0x0010, 0x0010), "AW1459205113.439.1243408275 ")  # * == dowolne imię
        else:
            id_key = gdcm.KeyValuePairType(gdcm.Tag(0x0010, 0x0010), patientID)  # * == dowolne imię

        study_id = gdcm.KeyValuePairType(gdcm.Tag(0x0020, 0x0010),"*")
        #klucze.append(id_key)
        klucze.append(study_id)

        # klucze.append(gdcm.KeyValuePairType(gdcm.Tag(0x0010, 0x0020), ""))
        print('Keys - READY! \n Makeing query....')
        # zwrotnie oczekujemy wypełnionego 10, 20 czyli PATIENT_ID

        # skonstruuj zapytanie gdcm.BaseRootQuery
        zapytanie = gdcm.CompositeNetworkFunctions.ConstructQuery(gdcm.eStudyRootType, gdcm.eStudy, klucze)
        print('Query - READY! \n Finding....')
        # sprawdź, czy zapytanie spełnia kryteria
        if not zapytanie.ValidateQuery():
            print("FIND błędne zapytanie!")
            return []

        # kontener na wyniki
        wynik = gdcm.DataSetArrayType()

        # wykonaj zapytanie
        stan = gdcm.CompositeNetworkFunctions.CFind(str(klient[2]), int(archive[3]), zapytanie, wynik, str(klient[1]),
                                                    str(archive[1]))

        # sprawdź stan
        if (not stan):
            print("Program isn't able to find any patients")
            return None
        if patientID is None:
            print("All patients are found")
        else:
            print("{} patient is found".format(patientID))
        response = []

        # pokaż wyniki
        for x in wynik:
            response.append([str(x.GetDataElement(gdcm.Tag(0x0020, 0x0010)).GetValue()),
                             str(x.GetDataElement(gdcm.Tag(0x0008, 0x0060)).GetValue())])
        return response


    @staticmethod
    def moveSeries(patientID:str = None):
        klient = db.get_active_user()
        archive = db.get_active_archive()

        # typ wyszukiwania(rozpoczynamy od pacjenta)
        type = gdcm.ePatientRootType

        # do jakiego poziomy wyszukujemy gdcm.EQueryLevel
        poziom = gdcm.ePatient # zobacz inne

        # klucze(filtrowanie lub określenie, które dane są potrzebne)
        klucze = gdcm.KeyValuePairArrayType()
        if patientID is not None:
            klucz1 = gdcm.KeyValuePairType(gdcm.Tag(0x0010, 0x0020), patientID) # NIE  WOLNO  TU STOSOWAC *; tutaj PatientID = "01"
        else:
           return []
        klucze.append(klucz1)

        # skonstruuj zapytanie
        zapytanie = gdcm.CompositeNetworkFunctions.ConstructQuery(type, poziom, klucze, gdcm.eMove)

        # sprawdź, czy zapytanie spełnia kryteria
        if (not zapytanie.ValidateQuery()):
            print("MOVE błędne zapytanie!")
            return

        # przygotuj katalog na wyniki String
        odebrane = '.images' # podkatalog odebrane w bieżącymkatalogu
        if (not os.path.exists(odebrane)): # jeśli nie istnieje
            os.mkdir(odebrane) # utwórz go String

        tmp = PACS_Action.__ran_gen(10)
        dane = os.path.join(odebrane,tmp)
        os.mkdir(dane) # wygeneruj losowąnazwępodkatalogu

        print(dane)
        print(str(klient[2]), int(klient[3]), zapytanie, int(archive[3]), str(klient[1]), str(archive[1]), dane)
        # wykonaj zapytanie - pobierzdo katalogu jak w zmiennej 'dane'
        stan = gdcm.CompositeNetworkFunctions.CMove(str(klient[2]), int(archive[3]), zapytanie, int(klient[3]), str(klient[1]), str(archive[1]),dane)

        # sprawdź  stan
        if not stan:
            print("MOVE nie działa!")
            return ''

        print("MOVE działa.")
        return dane

    @staticmethod
    def __ran_gen(size, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for x in range(size))

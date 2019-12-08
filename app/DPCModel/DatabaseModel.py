import sys
from datetime import date
from peewee import *

db = SqliteDatabase('res/dpc_data.db')

class DatabaseModel(Model):

    class Meta:
        database = db

class Archive(DatabaseModel):
    aec = CharField(null=False, unique=True)
    path = CharField(null=False)
    port = CharField(null=False)
    description = CharField(null = True)
    isActiv = BooleanField(null=False, default = False)

    class Meta:
        order_by=('aec',)

class User(DatabaseModel):
    aet = CharField(null=False, unique=False)
    port = CharField(null=False)
    adresIP = CharField(null=False)
    includeDate = DateField(null = False)
    isActiv = BooleanField(null=False, default=False)

    class Meta:
        order_by=('aec',)
# functions for database data management
def connectAndLoad():
    db.connect()  # connecting to db
    db.create_tables([Archive, User])  # creating tables
    _load_data()  # loading default data set
    return True

def _load_data():
    """ Przygotowanie początkowych danych testowych """
    if User.select().count() > 0:
        return

    archives = ['ARCHIWUM', r'c:\pacs\BAZA','10100', 'Opis ']
    users = (('KLIENTL', '127.0.0.1', '10104'),('KLIENT1', 'localhost', '10106'))

    o = Archive(aec=archives[0], path = archives[1], port = archives[2], description = archives[3], isActiv = True)
    o.save()
    for user in users:
        z = User(aet = user[0], adresIP = user[1], port = user[2], includeDate = date.today(), isActiv = False)
        z.save()
    db.commit()
    db.close()

def add_user(aet, adres, port):
    try:
        user = User.create(aet=str(aet),  port=str(port), adresIP=str(adres), includeDate=date.today())
    except:
        print("Unexpected error:", sys.exc_info()[0])

    finally:
        print('User added successful')

    return [aet, adres, port, date.today()]

def add_archive(aec, path, port, description):
    try:
        user = Archive.create(aec=str(aec),  path=str(path), port=str(port), description = str(description))
    except:
        print("Unexpected error:", sys.exc_info()[0])
    finally:
        print('User added successful')

    return [aec, path, port, description, date.today()]

def del_user(id):
    usr = get_active_user()
    if usr[0] != id:
        User.delete_by_id(id)
        return True
    else:
        return False

def del_archive(id):
    arch = get_active_archive()
    if arch[0] != id:
        Archive.delete_by_id(id)
        return True
    else:
        return False

def edit_user():
    #TODO
    return

def load_users():
    users = []
    usrDB = User.select()
    for z in usrDB:
        users.append([
            z.id,
            z.aet,
            z.adresIP,
            z.port,
            z.isActiv
            ])
    return users

def load_archives():
    archives = []
    archivesDB = Archive.select()
    for z in archivesDB:
        archives.append([
            z.id,
            z.aec,
            z.path,
            z.port,
            z.description,
            z.isActiv
            ])
    return archives

def get_active_user():
    if User.select().where(User.isActiv== 1).count() ==1:
        activUsr = User.get( User.isActiv == True)
        return [ activUsr.id, activUsr.aet, activUsr.adresIP, activUsr.port]
    else:
        return ['None','None','None','None']

def get_active_archive():
    if Archive.select().where(Archive.isActiv == 1).count() ==1:
        activArchive = Archive.get( Archive.isActiv == True)
        return [ activArchive.id, activArchive.aec, activArchive.path, activArchive.port]
    else:
        return ['None','None','None','None']

def set_active_user(id):
    if User.select().where(User.isActiv == 1).count() > 0 and User.select().where(User.isActiv == 1).count() == 1:
        user = User.select().where(User.isActiv == 1).get()

        user.isActiv = False
        user.save()

    usr = User.get_by_id(id)
    usr.isActiv = True
    usr.save()
    return True

def set_active_archive(id):
    if Archive.select().where(Archive.isActiv == 1).count() > 0 and Archive.select().where(Archive.isActiv == 1).count() == 1:
        archiv = Archive.select().where(Archive.isActiv == 1).get()

        archiv.isActiv = False
        archiv.save()

    arch = Archive.get_by_id(id)
    arch.isActiv = True
    arch.save()
    return True

from peewee import *
import datetime
from decimal import Decimal

pg_db = MySQLDatabase('superette', user='root', password='root',
                           host='localhost', port=3306)

class category(Model):
        category_name = CharField(null=True,unique=True)

        class Meta:
            database = pg_db 
    

class Produit(Model):
    nom = CharField(null=False)#il faut etre unique c'est trés important
    #category = ForeignKeyField(category , backref='category' , null=True)
    details = TextField(null=True)
    prix_achat = DecimalField(null=True)
    prix_vente= DecimalField()
    quantite = IntegerField()
    code = CharField(null=True)
   
    class Meta:
        database = pg_db

       
      
class Clients(Model):
    nom = CharField(unique=True)
    phone = CharField(null=True)
    date = DateTimeField(null=True)
    class Meta:
        database = pg_db

class Users(Model): 
    nom = CharField(null=True)
    password = CharField(null=True)
    class Meta:
        database = pg_db 

    
class Daily(Model):
    produit_daily = ForeignKeyField(Produit, backref='produit_daily')
    client_daily = ForeignKeyField(Clients, backref='client_daily')
    date = DateTimeField(null=True)
    user = ForeignKeyField(Users , backref='user')
    class Meta:
        database = pg_db

    
action_type = {(1,'historique_vente'),(2,'historique_vente')}

table_type = {(1,'produit'),
               (3,'clients'),
               (4,'categories'),
               (5,'users'),
               (6,'vente'),
               }
class Historique(Model):
    users = ForeignKeyField(Users,backref='users')
    action = CharField(choices=action_type,null=True)
    historique_vente = CharField(null=True) 
    historique_vente = CharField() 
    table = CharField(choices=table_type,null=True)
    date=DateTimeField(null=True)
    class Meta:
        database = pg_db


class Vente(Model):
    nouvel_vente = CharField(null=False)
    date = DateTimeField(null=True)
    class Meta:
        database = pg_db
class Achats(Model):
    nouvel_achat=CharField(null=True) 
    class Meta:
        database= pg_db   
    



pg_db.connection()    
t = pg_db.drop_tables([Produit,category,Users,Clients,Achats,Daily,Historique])
S = pg_db.create_tables([Produit,category,Users,Clients,Achats,Daily,Historique])


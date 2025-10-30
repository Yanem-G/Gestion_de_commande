# içi creer les tableaux
import sqlite3

db=sqlite3.connect("gestion.db")

db.execute("create table if not exists Produit(id_produit INTEGER PRIMARY KEY AUTOINCREMENT, nom text, prix integer, quantite_stock integer)")
db.execute("create table if not exists Client(id_client INTEGER PRIMARY KEY AUTOINCREMENT, nom text,contact text)")
db.execute("create table if not exists Commande(id_commande INTEGER PRIMARY KEY AUTOINCREMENT, id_client INTEGER, id_produit INTEGER, quantite integer, date_commande text)")
db.commit()


def insert_produit(nom,prix,qte):
    db.execute("insert into Produit(nom,prix,quantite_stock) values(?,?,?)",(nom,prix,qte))
    db.commit()

def update_produit(nom,prix,qte):
    db.execute("update Produit set prix=? , quantite_stock=? where nom=?", (prix,qte,nom))
    db.commit()

def delete_produit(nom):
    db.execute("delete from Produit where nom=?", (nom,))
    db.commit()

#Tests:
insert_produit("Ram",400,1)
update_produit("Ram",600,2)
insert_produit("CPY",400,1)
delete_produit("Ram")

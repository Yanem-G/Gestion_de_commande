# içi creer les tableaux
import sqlite3

db=sqlite3.connect("gestion.db")

db.execute("create table if not exists Produit(id_produit INTEGER PRIMARY KEY AUTOINCREMENT, nom text, prix integer, quantite_stock integer)")
db.execute("create table if not exists Client(id_client INTEGER PRIMARY KEY AUTOINCREMENT, nom text,contact text)")
db.execute("create table if not exists Commande(id_commande INTEGER PRIMARY KEY AUTOINCREMENT, id_client INTEGER, id_produit INTEGER, quantite integer, date_commande text)")
db.commit()

# fonction produit
def insert_produit(nom,prix,qte):
    db.execute("insert into Produit(nom,prix,quantite_stock) values(?,?,?)",(nom,prix,qte))
    db.commit()

def update_produit(nom,prix,qte):
    db.execute("update Produit set prix=? , quantite_stock=? where nom=?", (prix,qte,nom))
    db.commit()

def delete_produit(nom):
    db.execute("delete from Produit where nom=?", (nom,))
    db.commit()
# fonction client
def insert_client(nom,contact):
    db.execute("insert into Client(nom,contact) values(?,?)",(nom,contact))
    db.commit()

def update_client(nom,contact):
    db.execute("update Client set contact=? where nom=? ",(contact,nom))
    db.commit()

def delete_client(nom):
    db.execute("delete from Client where nom=?",(nom,))
    db.commit()
# fonction commande
def insert_commande(nom_client,nom_produit,quantite):
    db.row_factory=sqlite3.Row
    cursor_produit = db.execute("select id_produit from Produit where nom=?",(nom_produit,))
    cursor_client = db.execute("select id_client from Client where nom=?",(nom_client,))
    cursor_datetime = db.execute("SELECT datetime('now')")

    row_produit = cursor_produit.fetchone()
    row_client = cursor_client.fetchone()
    row_datetime = cursor_datetime.fetchone() #retourne un tuple = ('datetime',)
    db.execute("insert into Commande(id_client,id_produit,quantite,date_commande) values(?,?,?,?)",(row_client["id_client"],row_produit["id_produit"],quantite,row_datetime[0]))
    db.commit()

def update_commande(id_commande,quantite):
    db.execute("update Commande set quantite=? where id_commande=? ",(quantite,id_commande))
    db.commit()

def delete_commande(id_commande):
    db.execute("delete from Commande where id_commande=?",(id_commande,))
    db.commit()

#Tests:
insert_produit("Ram",400,1)
update_produit("Ram",600,2)
insert_produit("CPY",400,1)


insert_client("Aymen","0615478454")
insert_client("Abdessamad","0798653256")
insert_client("Marwane","0712457898")
update_client("Abdessamad","0698989898")
delete_client("Aymen")

insert_commande("Marwane","CPY",1)
insert_commande("Abdessamad","Ram",1)
update_commande(1,2)
delete_commande(2)
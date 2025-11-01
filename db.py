# içi creer les tableaux
import sqlite3

def create_tables(db):
    db.execute("create table if not exists Produit(id_produit INTEGER PRIMARY KEY AUTOINCREMENT, nom text, prix integer, quantite_stock integer)")
    db.execute("create table if not exists Client(id_client INTEGER PRIMARY KEY AUTOINCREMENT, nom text,contact text)")
    db.execute("create table if not exists Commande(id_commande INTEGER PRIMARY KEY AUTOINCREMENT, id_client INTEGER, id_produit INTEGER, quantite integer, date_commande text)")
    db.commit()

# fonction produit
def insert_produit(db,nom,prix,qte):
    db.execute("insert into Produit(nom,prix,quantite_stock) values(?,?,?)",(nom,prix,qte))
    db.commit()

def update_produit(db,nom,prix,qte):
    db.execute("update Produit set prix=? , quantite_stock=? where nom=?", (prix,qte,nom))
    db.commit()

def delete_produit(db,nom):
    db.execute("delete from Produit where nom=?", (nom,))
    db.commit()
# fonction client
def insert_client(db,nom,contact):
    db.execute("insert into Client(nom,contact) values(?,?)",(nom,contact))
    db.commit()

def update_client(db,nom,contact):
    db.execute("update Client set contact=? where nom=? ",(contact,nom))
    db.commit()

def delete_client(db,nom):
    db.execute("delete from Client where nom=?",(nom,))
    db.commit()
# fonction commande
def insert_commande(db,nom_client,nom_produit,quantite):
    # (On a supprimé db.row_factory)
    cursor_produit = db.execute("select id_produit from Produit where nom=?",(nom_produit,))
    cursor_client = db.execute("select id_client from Client where nom=?",(nom_client,))
    cursor_datetime = db.execute("SELECT datetime('now')")

    row_produit = cursor_produit.fetchone()
    row_client = cursor_client.fetchone()
    row_datetime = cursor_datetime.fetchone() #retourne un tuple = ('datetime',)
    db.execute("insert into Commande(id_client,id_produit,quantite,date_commande) values(?,?,?,?)",(row_client[0],row_produit[0],quantite,row_datetime[0]))
    db.commit()

def update_commande(db,nom_client,nom_produit,quantite):
    # (On a supprimé db.row_factory)
    cursor_produit = db.execute("select id_produit from Produit where nom=?",(nom_produit,))
    cursor_client = db.execute("select id_client from Client where nom=?",(nom_client,))

    row_produit = cursor_produit.fetchone()
    row_client = cursor_client.fetchone()

    cursor_commande = db.execute("SELECT id_commande FROM Commande where id_client=? AND id_produit=?",(row_client[0],row_produit[0]))
    row_commande = cursor_commande.fetchone()

    db.execute("update Commande set quantite=? where id_commande=? ",(quantite,row_commande[0]))
    db.commit()

def delete_commande(db,nom_client,nom_produit,quantite):
    # (On a supprimé db.row_factory)
    cursor_produit = db.execute("select id_produit from Produit where nom=?",(nom_produit,))
    cursor_client = db.execute("select id_client from Client where nom=?",(nom_client,))

    row_produit = cursor_produit.fetchone()
    row_client = cursor_client.fetchone()

    cursor_commande = db.execute("SELECT id_commande FROM Commande where id_client=? AND id_produit=?",(row_client[0],row_produit[0]))
    row_commande = cursor_commande.fetchone()

    db.execute("delete from Commande where id_commande=? AND quantite=?",(row_commande[0],quantite))
    db.commit()

#Tests:
if __name__ == "__main__":
    # Ce code ne s'exécute QUE si tu lances db.py directement
    
    # On crée une connexion juste pour les tests
    db_test = sqlite3.connect("gestion_test.db") 
    create_tables(db_test)
    insert_produit(db_test,"Ram",400,1)
    update_produit(db_test,"Ram",600,2)
    insert_produit(db_test,"CPY",400,1)


    insert_client(db_test,"Aymen","0615478454")
    insert_client(db_test,"Abdessamad","0798653256")
    insert_client(db_test,"Marwane","0712457898")
    update_client(db_test,"Abdessamad","0698989898")
    delete_client(db_test,"Aymen")

    insert_commande(db_test,"Marwane","CPY",1)
    insert_commande(db_test,"Abdessamad","Ram",1)
    update_commande(db_test,"Marwane","CPY",5)
    delete_commande(db_test,"Abdessamad","Ram",1)
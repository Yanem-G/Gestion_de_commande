# içi creer les tableaux
import sqlite3

db=sqlite3.connect("gestion.db")

db.execute("create table if not exists Produit(id_produit integer, nom text, prix integer, quantite_stock integer)")
from tkinter import *
from tkinter import ttk
import sqlite3
import db as db_operations

db=sqlite3.connect("gestion.db")

window = Tk()

window.title("Gestion des commands")
window.geometry("1000x600")
window.minsize(1000,600)
window.config(background="#FFFFFF")


def show_frame(frame):
    for f in [produits_frame,clients_frame,commandes_frame]:
        f.forget()#gadi nsado ga3 les frames o n7alo libghina
    frame.pack(side=LEFT,fill="both")


def updateTable(trv, table):
    #Vider le tableau avant de remplir
    for item in trv.get_children():
        trv.delete(item)
    # probleme d'affichage de la table commande
    if table == 'Commande':
        query = """
        SELECT 
            Commande.id_commande, 
            Client.nom, 
            Produit.nom, 
            Commande.quantite, 
            Commande.date_commande 
        FROM Commande
        JOIN Client ON Commande.id_client = Client.id_client
        JOIN Produit ON Commande.id_produit = Produit.id_produit
        """
        data = db.execute(query)
        
        # (Assurez-vous que vos en-têtes de tableau correspondent !)
        trv.heading(2, text="Client")
        trv.heading(3, text="Produit")

    else:
        # Requête normale pour les tables Produit et Client
        data = db.execute(f'SELECT * FROM {table}')

    for row in data.fetchall():
        trv.insert('',END,values=row)






menu_frame = Frame(window,width=200,height=500,bg="#C2E2FA")
menu_frame.pack(side=LEFT,fill="y")

produits_Btn = Button(menu_frame,text="Produits",font=("fourrier",13), width=20 , pady=10 , command=lambda:show_frame(produits_frame))
produits_Btn.grid(row=1 , column=1 , padx=20,pady=10)

produits_Btn = Button(menu_frame,text="Clients",font=("fourrier",13), width=20 , pady=10 , command=lambda:show_frame(clients_frame))
produits_Btn.grid(row=2 , column=1 , padx=20,pady=20)

produits_Btn = Button(menu_frame,text="Commandes",font=("fourrier",13), width=20 , pady=10 , command=lambda:show_frame(commandes_frame))
produits_Btn.grid(row=3 , column=1 , padx=20,pady=20)

produits_Btn = Button(menu_frame,text="Quit",font=("fourrier",13), width=20 , pady=10 , command=window.quit)
produits_Btn.grid(row=4 , column=1 , padx=20,pady=20)







####Tables style#####
style=ttk.Style()
style.configure("Treeview.Heading",font=("courrier",12))
style.configure("Treeview",font=("courrier",11))







######### Frame Produits ###################################
produits_frame=Frame(window, bg="white",padx=10, pady=20)
produits_frame.pack(side=LEFT,fill="both")

titre_produits = Label(produits_frame,text="Produits",font=("courrier", 20, "bold") , background="#ffffff")
titre_produits.pack(anchor='w')

#Tableau
trv_produit=ttk.Treeview(produits_frame,columns=(1,2,3,4),height=10,show="headings")

trv_produit.column(1,width=50,anchor=CENTER)
trv_produit.column(2,width=200,anchor=CENTER)
trv_produit.column(3,width=150,anchor=CENTER)
trv_produit.column(4,width=230,anchor=CENTER)

trv_produit.heading(1,text="ID")
trv_produit.heading(2,text="Nom")
trv_produit.heading(3,text="Prix")
trv_produit.heading(4,text="Quantité en stock")

trv_produit.pack()

updateTable(trv_produit,table='Produit')
#Fin Tableau

form_produit = Frame(produits_frame,bg="white")
form_produit.grid_columnconfigure(1, weight=1) # les widget dans la colonne 1 vont pouvoir prendre tout l'espace disponible
form_produit.pack(padx=10,pady=10,fill="x")

com1=Label(form_produit,text="Nom:",font=("courrier", 20, "bold") , background="#ffffff")
com1.grid(column=0,row=0)
com2=Label(form_produit,text="Quantite:",font=("courrier", 20, "bold") , background="#ffffff")
com2.grid(column=0,row=1)
com3=Label(form_produit,text="Prix:",font=("courrier", 20, "bold") , background="#ffffff")
com3.grid(column=0,row=2)

prod_entry1 = Entry(form_produit,font=("courrier", 20, "bold") , background="#ffffff")
prod_entry1.grid(column=1,row=0,sticky="ew", columnspan=2) # columnspan dit au grid de sétirer sur la colonne 2
prod_entry2 = Entry(form_produit,font=("courrier", 20, "bold") , background="#ffffff")
prod_entry2.grid(column=1,row=1,sticky="ew", columnspan=2)
prod_entry3 = Entry(form_produit,font=("courrier", 20, "bold") , background="#ffffff")
prod_entry3.grid(column=1,row=2,sticky="ew", columnspan=2)

# Les fonctions des boutons
def ajouter_produit():
    nom = prod_entry1.get()
    quantite = int(prod_entry2.get())
    prix = float(prod_entry3.get())
    
    db_operations.insert_produit(db,nom,prix,quantite)

    #on met a jour la table
    updateTable(trv_produit,table='Produit')
def modifier_produit():
    nom = prod_entry1.get()
    quantite = int(prod_entry2.get())
    prix = float(prod_entry3.get())
    
    db_operations.update_produit(db,nom,prix,quantite)

    #on met a jour la table
    updateTable(trv_produit,table='Produit')
def supprimmer_produit():
    nom = prod_entry1.get()
    
    db_operations.delete_produit(db,nom)

    #on met a jour la table
    updateTable(trv_produit,table='Produit')

prod_bouton1= Button(form_produit,text="Ajouter un produit",font=("fourrier",13),width=20,pady=10,command=ajouter_produit)
prod_bouton1.grid(column=0,row=4,pady=10,padx=10)
prod_bouton2 = Button(form_produit,text="Modifier un produit",font=("fourrier",13),width=20,pady=10,command=modifier_produit)
prod_bouton2.grid(column=1,row=4,pady=10,padx=10)
prod_bouton3 = Button(form_produit,text="Supprimmer un produit",font=("fourrier",13),width=20,pady=10,command=supprimmer_produit)
prod_bouton3.grid(column=2,row=4,pady=10,padx=10)


def on_select(event):
    selected_item = trv_produit.focus()
    if not selected_item:
        return
    values = trv_produit.item(selected_item, 'values')
    
    # Clear old data
    prod_entry1.delete(0, END)
    prod_entry2.delete(0, END)
    prod_entry3.delete(0, END)
    
    # Fill with new data
    prod_entry1.insert(0, values[1])
    prod_entry2.insert(0, values[3])
    prod_entry3.insert(0, values[2])

#  Bind Treeview selection event 
trv_produit.bind("<<TreeviewSelect>>", on_select)
#############################################################












######### Frame Clinets ###################################
clients_frame=Frame(window, bg="white",padx=10, pady=20)
produits_frame.pack(side=LEFT,fill="both")

titre_client = Label(clients_frame,text="Clients",font=("courrier", 20, "bold") , background="#ffffff")
titre_client.pack(anchor='w')

#Tableau:
trv_client=ttk.Treeview(clients_frame,columns=(1,2,3),height=10,show="headings")

trv_client.column(1,width=50,anchor=CENTER)
trv_client.column(2,width=200,anchor=CENTER)
trv_client.column(3,width=250,anchor=CENTER)

trv_client.heading(1,text="ID")
trv_client.heading(2,text="Nom")
trv_client.heading(3,text="Contact")

trv_client.pack()

updateTable(trv_client,table='Client')
#Fin Tableau

form_client = Frame(clients_frame,bg="white")
form_client.grid_columnconfigure(1, weight=1) # les widget dans la colonne 1 vont pouvoir prendre tout l'espace disponible
form_client.pack(padx=10,pady=10,fill="x")

com1=Label(form_client,text="Nom:",font=("courrier", 20, "bold") , background="#ffffff")
com1.grid(column=0,row=0)
com2=Label(form_client,text="contact:",font=("courrier", 20, "bold") , background="#ffffff")
com2.grid(column=0,row=1)

client_entry1 = Entry(form_client,font=("courrier", 20, "bold") , background="#ffffff")
client_entry1.grid(column=1,row=0,sticky="ew", columnspan=2) # columnspan dit au grid de sétirer sur la colonne 2
client_entry2 = Entry(form_client,font=("courrier", 20, "bold") , background="#ffffff")
client_entry2.grid(column=1,row=1,sticky="ew", columnspan=2)

# Les fonctions des boutons
def ajouter_client():
    nom = client_entry1.get()
    contact = client_entry2.get()
    
    db_operations.insert_client(db,nom,contact)

    #on met a jour la table
    updateTable(trv_client,table='Client')
def modifier_client():
    nom = client_entry1.get()
    contact = client_entry2.get()
    
    db_operations.update_client(db,nom,contact)

    #on met a jour la table
    updateTable(trv_client,table='Client')
def supprimmer_client():
    nom = client_entry1.get()
    
    db_operations.delete_client(db,nom)

    #on met a jour la table
    updateTable(trv_client,table='Client')

client_bouton1= Button(form_client,text="Ajouter un client",font=("fourrier",13),width=20,pady=10,command=ajouter_client)
client_bouton1.grid(column=0,row=4,pady=10,padx=10)
client_bouton2 = Button(form_client,text="Modifier un client",font=("fourrier",13),width=20,pady=10,command=modifier_client)
client_bouton2.grid(column=1,row=4,pady=10,padx=10)
client_bouton3 = Button(form_client,text="Supprimmer un client",font=("fourrier",13),width=20,pady=10,command=supprimmer_client)
client_bouton3.grid(column=2,row=4,pady=10,padx=10)


def on_select(event):
    selected_item = trv_client.focus() 
    if not selected_item: 
        return
    values = trv_client.item(selected_item, 'values')
    
    # Clear old data
    client_entry1.delete(0, END)
    client_entry2.delete(0, END)
    
    # Fill with new data
    client_entry1.insert(0, values[1])
    client_entry2.insert(0, values[2])

#  Bind Treeview selection event 
trv_client.bind("<<TreeviewSelect>>", on_select)
#############################################################









######### Frame Commandes ###################################
commandes_frame=Frame(window, bg="white",padx=10, pady=20)
produits_frame.pack(side=LEFT,fill="both")

titre_produits = Label(commandes_frame,text="Commandes",font=("courrier", 20, "bold") , background="#ffffff")
titre_produits.pack(anchor='w')

#Tableau
trv_commande=ttk.Treeview(commandes_frame,columns=(1,2,3,4,5),height=10,show="headings")

trv_commande.column(1,width=50,anchor=CENTER)
trv_commande.column(2,width=150,anchor=CENTER)
trv_commande.column(3,width=100,anchor=CENTER)
trv_commande.column(4,width=150,anchor=CENTER)
trv_commande.column(5,width=200,anchor=CENTER)

trv_commande.heading(1,text="ID")
trv_commande.heading(2,text="Id client")
trv_commande.heading(3,text="Id produit")
trv_commande.heading(4,text="Quantite")
trv_commande.heading(5,text="Date_commande")

trv_commande.pack()

updateTable(trv_commande,table='Commande')
#Fin Tableau
form_commande = Frame(commandes_frame,bg="white")
form_commande.grid_columnconfigure(1, weight=1) # les widget dans la colonne 1 vont pouvoir prendre tout l'espace disponible
form_commande.pack(padx=10,pady=10,fill="x")

com1=Label(form_commande,text="Client:",font=("courrier", 20, "bold") , background="#ffffff")
com1.grid(column=0,row=0)
com2=Label(form_commande,text="Produit:",font=("courrier", 20, "bold") , background="#ffffff")
com2.grid(column=0,row=1)
com3=Label(form_commande,text="Quantite:",font=("courrier", 20, "bold") , background="#ffffff")
com3.grid(column=0,row=2)

comm_entry1 = Entry(form_commande,font=("courrier", 20, "bold") , background="#ffffff")
comm_entry1.grid(column=1,row=0,sticky="ew", columnspan=2) # columnspan dit au grid de sétirer sur la colonne 2
comm_entry2 = Entry(form_commande,font=("courrier", 20, "bold") , background="#ffffff")
comm_entry2.grid(column=1,row=1,sticky="ew", columnspan=2)
comm_entry3 = Entry(form_commande,font=("courrier", 20, "bold") , background="#ffffff")
comm_entry3.grid(column=1,row=2,sticky="ew", columnspan=2)

# Les fonctions des boutons
def ajouter_commande():
    client = comm_entry1.get()
    produit = comm_entry2.get()
    quantite = int(comm_entry3.get())
    
    db_operations.insert_commande(db,client,produit,quantite)

    #on met a jour la table
    updateTable(trv_commande,table='Commande')
def modifier_commande():
    client = comm_entry1.get()
    produit = comm_entry2.get()
    quantite = int(comm_entry3.get())
    
    db_operations.update_commande(db,client,produit,quantite)

    #on met a jour la table
    updateTable(trv_commande,table='Commande')
def supprimmer_commande():
    client = comm_entry1.get()
    produit = comm_entry2.get()
    quantite = int(comm_entry3.get())
    
    db_operations.delete_commande(db,client,produit,quantite)

    #on met a jour la table
    updateTable(trv_commande,table='Commande')

comm_bouton1= Button(form_commande,text="Ajouter une commande",font=("fourrier",13),pady=10,command=ajouter_commande)
comm_bouton1.grid(column=0,row=4,pady=10,padx=5)
comm_bouton2 = Button(form_commande,text="Modifier une commande",font=("fourrier",13),pady=10,command=modifier_commande)
comm_bouton2.grid(column=1,row=4,pady=10,padx=5)
comm_bouton3 = Button(form_commande,text="Supprimmer une commande",font=("fourrier",13),pady=10,command=supprimmer_commande)
comm_bouton3.grid(column=2,row=4,pady=10,padx=5)


def on_select(event):
    selected_item = trv_commande.focus()
    if not selected_item:
        return
    values = trv_commande.item(selected_item, 'values')
    
    # Clear old data
    comm_entry1.delete(0, END)
    comm_entry2.delete(0, END)
    comm_entry3.delete(0, END)
    
    # Fill with new data
    comm_entry1.insert(0, values[1])
    comm_entry2.insert(0, values[2])
    comm_entry3.insert(0, values[3])

#  Bind Treeview selection event 
trv_commande.bind("<<TreeviewSelect>>", on_select)

#############################################################




window.mainloop()
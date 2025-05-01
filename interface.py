import tkinter as tk
from tkinter import *
try:
    import budget
    print("Module budget importé avec succès")
except ModuleNotFoundError as e:
    print(f"Erreur d'importation : {e}")

import sqlite3

"""def afficher_transactions():
    transactions = budget.df_transactions  # Récupérer le DataFrame
    text_widget.delete("1.0", tk.END)  # Vider l'affichage précédent
    text_widget.insert(tk.END, transactions.to_string())  # Afficher les données

def afficher_revenus():
    revenus = budget.df_revenus  # Récupérer le DataFrame
    text_widget.delete("1.0", tk.END)  # Vider l'affichage précédent
    text_widget.insert(tk.END, revenus.to_string())  # Afficher les données

def afficher_depenses():
    depenses = budget.df_depenses  # Récupérer le DataFrame
    text_widget.delete("1.0", tk.END)  # Vider l'affichage précédent
    text_widget.insert(tk.END, depenses.to_string())  # Afficher les données"""

# Création de la fenêtre principale
root = tk.Tk()
root.title("Gestion de Budget")
root.geometry("500x500")

tk.Label(root, text="ID").pack()
entry_id= Entry(root)
entry_id.pack()

tk.Label(root, text="Date (YYYY-MM-DD)").pack()
entry_date= Entry(root)
entry_date.pack()

tk.Label(root, text="Catégorie ID").pack()
entry_categorie_id = Entry(root)
entry_categorie_id.pack()

tk.Label(root, text="Montant").pack()
entry_montant= Entry(root)
entry_montant.pack()

tk.Label(root, text="Type (revenu/depense)").pack()
entry_type= Entry(root)
entry_type.pack()

tk.Label(root, text="Description").pack()
entry_description= Entry(root)
entry_description.pack()

text_widget=Text(root,height=15,width=80)

def ajouter_transactions():

    id = entry_id.get()
    date = entry_date.get()
    categorie_id = entry_categorie_id.get()
    montant = entry_montant.get()
    type = entry_type.get()
    description = entry_description.get()
    if id and date and montant and type and description :
        con = sqlite3.connect("budget.db", check_same_thread=False)
        cur = con.cursor()
        cur.execute("""INSERT INTO transactions(id,date,categorie_id,montant,type,description) VALUES(?,?,?,?,?,?) ON CONFLICT(id) DO NOTHING; """,(id,date,categorie_id,montant,type,description))
        con.commit()
        con.close()
        entry_id.delete(0, END)
        entry_date.delete(0, END)
        entry_categorie_id.delete(0,END)
        entry_montant.delete(0, END)
        entry_type.delete(0, END)
        entry_description.delete(0, END)

def Afficher_transactions():
    con = sqlite3.connect("budget.db",check_same_thread=False)
    cur=con.cursor()
    cur.execute("SELECT * FROM transactions")
    transactions = cur.fetchall()
    con.close()
    text_widget.delete("1.0",END)

    for transaction in transactions:
        text_widget.insert(END,str(transaction)+"\n")
        print(text_widget)  

        

# Bouton pour afficher les transactions
btn_ajouter_trans = tk.Button(root, text="Ajouter Transactions", command=ajouter_transactions)
btn_ajouter_trans.pack()
btn_afficher_trans = tk.Button(root, text="Afficher Transactions", command=Afficher_transactions)
btn_afficher_trans.pack()

"""btn_afficher_rev = tk.Button(root, text="Afficher Revenus", command=afficher_revenus)
btn_afficher_rev.pack()

btn_afficher_dep = tk.Button(root, text="Afficher Depenses", command=afficher_depenses)
btn_afficher_dep.pack()"""

# Zone de texte pour afficher les transactions
"""entry_id = tk.Entry(root, height=20, width=80)
entry_id.pack()
entry_date = tk.Entry(root, height=20, width=80)
entry_date.pack()
entry_montant = tk.Entry(root, height=20, width=80)
entry_montant.pack()
entry_type = tk.Text(root, height=20, width=80)
entry_type.pack()
entry_categorie = tk.Text(root, height=20, width=80)
entry_categorie.pack()"""

# Lancer l'interface
root.mainloop()

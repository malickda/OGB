import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

con = sqlite3.connect("budget.db")
cur = con.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS transactions (
    id INT NOT NULL PRIMARY KEY,
    date TEXT,
    categorie_id INT,
    montant REAL,
    type TEXT,
    description TEXT
);
""")

cur.execute("""CREATE TABLE IF NOT EXISTS categories (
    id INT NOT NULL PRIMARY KEY,
    nom TEXT
);
""")

cur.execute("""CREATE TABLE IF NOT EXISTS revenus (
    id INT NOT NULL PRIMARY KEY,
    date TEXT,
    montant REAL,
    description TEXT
);
""")

cur.execute("""CREATE TABLE IF NOT EXISTS depenses (
    id INT NOT NULL PRIMARY KEY,
    date TEXT,
    montant REAL,
    description TEXT
);
""")

cur.execute("""INSERT INTO transactions VALUES
    ('1','2023-09-25','21','75','depense','loisir'),
    ('2','2023-10-30','22','300','revenu','salaire'),
    ('3','2023-10-31','23','100','depense','course alimentaire'),
    ('4','2023-11-01','24','30','depense','preté'),
    ('5','2023-11-05','25','60','depense','transport'),
    ('6','2023-11-15','26','100','revenu','parents'),
    ('7','2023-11-22','27','30','revenu','pret remboursé'),
    ('8','2023-11-30','28','300','revenu','salaire')
    ON CONFLICT(id) DO NOTHING;
""")

cur.execute("""INSERT INTO categories VALUES
    ('1','loisir'),
    ('2','salaire'),
    ('3','alimentaire'),
    ('4','preté'),
    ('5','transport'),
    ('6','parents'),
    ('7','pret remboursé'),
    ('8','salaire')
    ON CONFLICT(id) DO NOTHING;
""")

cur.execute("""INSERT INTO revenus VALUES
    ('2','2023-10-30','300','cours a domicile'),
    ('6','2023-11-15','100','parents'),
    ('7','2023-11-22','30','pret remboursé'),
    ('8','2023-11-30','300','salaire')
    ON CONFLICT(id) DO NOTHING;
""")

cur.execute("""INSERT INTO depenses VALUES
    ('1','2023-09-25','75','loisir'),
    ('3','2023-10-31','100','course alimentaire'),
    ('4','2023-11-01','30','preté'),
    ('5','2023-11-05','60','transport')
    ON CONFLICT(id) DO NOTHING;
""")

id_to_delete = 10
cur.execute("DELETE FROM transactions WHERE id = ?;", (id_to_delete,))

df_transactions = pd.read_sql_query("SELECT * FROM transactions", con)
df_categories = pd.read_sql_query("SELECT * FROM categories", con)
df_revenus = pd.read_sql_query("SELECT * FROM revenus", con)
df_depenses = pd.read_sql_query("SELECT * FROM depenses", con)

# Regroupement par mois
df_transactions['date'] = pd.to_datetime(df_transactions['date'], format='%Y-%m-%d')
df_revenus['date'] = pd.to_datetime(df_revenus['date'], format='%Y-%m-%d')
df_depenses['date'] = pd.to_datetime(df_depenses['date'], format='%Y-%m-%d')

# Ajouter une colonne "mois"
df_transactions["mois"] = df_transactions["date"].dt.to_period("M")
df_revenus["mois"] = df_revenus["date"].dt.to_period("M")
df_depenses["mois"] = df_depenses["date"].dt.to_period("M")

# Regrouper par mois et sommer les montants
df_transactions_grouped = df_transactions.groupby("mois")["montant"].sum()
df_revenus_grouped = df_revenus.groupby("mois")["montant"].sum()
df_depenses_grouped = df_depenses.groupby("mois")["montant"].sum()

"""print(df_transactions_grouped.head)
print(df_depenses_grouped.head)
print(df_revenus_grouped.head)"""

df_transactions_grouped.index = df_transactions_grouped.index.astype(str)
df_revenus_grouped.index = df_revenus_grouped.index.astype(str)
df_depenses_grouped.index = df_depenses_grouped.index.astype(str)

"""print("Transactions par date")
print(df_transactions)
print("Revenus par date")
print(df_revenus)
print("Dépenses par date")
print(df_depenses)"""


"""plt.figure(figsize=(10, 5))
plt.plot(df_transactions["date"], df_transactions["montant"], label="Transactions")
plt.legend()
plt.xticks(rotation=45)
plt.xlabel("date")
plt.ylabel("Montant")
plt.show()

plt.figure(figsize=(10, 5))
plt.plot(df_revenus["date"], df_revenus["montant"], label="Revenus")
plt.legend()
plt.xticks(rotation=45)
plt.xlabel("date")
plt.ylabel("Montant")
plt.show()

plt.figure(figsize=(10, 5))
plt.plot(df_depenses["date"], df_depenses["montant"], label="Dépenses")
plt.legend()
plt.xticks(rotation=45)
plt.xlabel("date")
plt.ylabel("Montant")

plt.show()"""

#print(len(df_transactions_grouped["mois"]), len(df_transactions_grouped["montant"]))
#print(df_transactions_grouped["mois"].shape, df_transactions_grouped["montant"].shape)



"""plt.figure(figsize=(10, 5))
plt.plot(df_transactions_grouped.index, df_transactions_grouped.values, label="Transactions")
plt.legend()
plt.xticks(rotation=45)
plt.xlabel("Mois")
plt.ylabel("Montant")
plt.show()

plt.figure(figsize=(10, 5))
plt.plot(df_revenus_grouped.index, df_revenus_grouped.values, label="Revenus")
plt.legend()
plt.xticks(rotation=45)
plt.xlabel("Mois")
plt.ylabel("Montant")
plt.show()

plt.figure(figsize=(10, 5))
plt.plot(df_depenses_grouped.index, df_depenses_grouped.values, label="Dépenses")
plt.legend()
plt.xticks(rotation=45)
plt.xlabel("Mois")
plt.ylabel("Montant")

plt.show()"""

con.commit()
con.close()

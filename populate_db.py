from models.database import Database
from datetime import datetime, timedelta
import random

db = Database()
conn = db.conn

# Ajouter 3 sources
sources = [("JIRAMA", 0.25), ("Groupe", 0.6), ("Solaire", 0.1)]
for nom, cout in sources:
    conn.execute("INSERT OR IGNORE INTO sources (nom, cout_kwh) VALUES (?, ?)", (nom, cout))

# Ajouter 4 types d'équipements
types_eq = ["Éclairage", "Climatisation", "Informatique", "Réfrigérateur"]
for t in types_eq:
    conn.execute("INSERT OR IGNORE INTO types_equipements (nom) VALUES (?)", (t,))

# Ajouter 5 équipements
equipements = [
    ("Lampe Salle 101", 1),
    ("Lampe Bureau", 1),
    ("Clim Bureau", 2),
    ("PC Admin", 3),
    ("Frigo Cuisine", 4)
]
for nom, type_id in equipements:
    conn.execute("INSERT OR IGNORE INTO equipements (nom, type_id) VALUES (?, ?)", (nom, type_id))

# Ajouter consommation aléatoire pour 7 derniers jours
for jour in range(7):
    date = datetime.now() - timedelta(days=jour)
    for eq_id in range(1, 6):
        for src_id in range(1, 4):
            kwh = random.uniform(0.5, 5.0)
            conn.execute("INSERT INTO consommation (equipement_id, source_id, kwh, date) VALUES (?, ?, ?, ?)",
                         (eq_id, src_id, kwh, date))
            
# Ajouter une coupure d'exemple
debut = datetime.now() - timedelta(days=1, hours=3)
fin = datetime.now() - timedelta(days=1, hours=1)
conn.execute("INSERT INTO coupures (debut, fin, duree) VALUES (?, ?, ?)",
             (debut, fin, 2))

conn.commit()
print("Base remplie avec données fictives ")

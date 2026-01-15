from models.consommation_model import ConsommationModel
from models.source_model import SourceModel
from models.equipement_model import EquipementModel
from datetime import datetime, timedelta

class EnergieController:
    
    def __init__(self):
        self.consommation_model = ConsommationModel()
        self.source_model = SourceModel()
        self.equipement_model = EquipementModel()

    def consommation_cumulee(self, periode="jour"):
        cursor = self.consommation_model.conn.cursor()

        if periode == "jour":
            delta = 1
        elif periode == "semaine":
            delta = 7
        else:
            delta = 30

        date_limite = datetime.now() - timedelta(days=delta)

        cursor.execute("""
        SELECT SUM(kwh) as total
        FROM consommation
        WHERE date >= ?
        """, 
        (date_limite,)
        )

        result = cursor.fetchone()
        return result["total"] if result["total"] else 0
    
    def detecter_anomalie(self, seuil_kwh):
        cursor = self.consommation_model.conn.cursor()

        cursor.execute("""
        SELECT equipement_id, SUM(kwh) as total
        FROM consommation
        GROUP BY equipement_id
        HAVING total > ?
        """, 
        (seuil_kwh,)
        )
        return cursor.fetchall()

    def cout_par_source(self):
        cursor = self.consommation_model.conn.cursor()

        cursor.execute("""
        SELECT s.nom, SUM(c.kwh * s.cout_kwh) AS cout_total
        FROM consommation c
        JOIN sources s ON c.source_id = s.id
        GROUP BY s.nom
        """)
        return cursor.fetchall()
    
    def simulation_coupure(self, duree_heures):
        return f"Coupure JIRAMA detectee : bascule sur groupe electrogene pendant {duree_heures}h"
    
    # detecte les equipements gourmand
    def alertes_consommation(self, seuil_kwh):
        cursor = self.consommation_model.conn.cursor()
        cursor.execute("""
        SELECT e.nom, SUM(c.kwh) AS total
        FROM consommation c
        JOIN equipements e ON c.equipement_id = e.id
        GROUP BY e.nom
        HAVING total > ?
        """,
        (seuil_kwh,)
        )
        return cursor.fetchall()
    
    def consommation_pendant_coupure(self):
        cursor = self.consommation_model.conn.cursor()
        cursor.execute("""
        SELECT c.date, c.kwh
        FROM consommation c
        JOIN coupures cp
        ON c.date BETWEEN cp.debut AND cp.fin
        """)
        return cursor.fetchall()
    
    def enregistrer_coupure(self, debut, fin):
        duree = (fin - debut).total_seconds() / 3600
        cursor = self.consommation_model.conn.cursor()
        cursor.execute("""
        INSERT INTO coupures (debut, fin, duree)
        VALUES (?, ?, ?)
        """,
        (debut, fin, duree)
        )
        self.consommation_model.conn.commit()
    
    def consommation_par_source_graph(self):
        cursor = self.consommation_model.conn.cursor()
        cursor.execute("""
        SELECT s.nom, SUM(c.kwh) AS total
        FROM consommation c
        JOIN sources s ON c.source_id = s.id
        GROUP BY s.nom
        """)
        return cursor.fetchall()

    def score_efficacite(self):
        cursor = self.consommation_model.conn.cursor()
        cursor.execute("SELECT SUM(kwh) FROM consommation")
        total = cursor.fetchone()[0] or 0

        if total < 50:
            return "🟢 Très efficace"
        elif total < 150:
            return "🟠 Moyenne"
        else:
            return "🔴 Mauvaise efficacité"

    def historique_coupures(self):
        cursor = self.consommation_model.conn.cursor()
        cursor.execute("""
            SELECT debut, fin, duree
            FROM coupures
            ORDER BY debut DESC
        """)
        return cursor.fetchall()
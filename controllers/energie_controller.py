from models.consommation_model import ConsommationModel
from models.source_model import SourceModel
from models.equipement_model import EquipementModel
from datetime import datetime, timedelta

class EnergieController:
    def __init__(self):
        self.consommation_model = ConsommationModel()
        self.source_model = SourceModel()
        self.equipement_model = EquipementModel()

    def consommation_cumulee(self):
        cursor = self.consommation_model.conn.cursor()
        cursor.execute("SELECT SUM(kwh) AS total FROM consommation")
        result = cursor.fetchone()[0]
        return result if result else 0

    def score_efficacite(self):
        total = self.consommation_cumulee()
        if total < 50:
            return "🟢 Très efficace"
        elif total < 150:
            return "🟠 Moyenne"
        else:
            return "🔴 Mauvaise efficacité"

    def alertes_consommation(self, seuil_kwh):
        cursor = self.consommation_model.conn.cursor()
        cursor.execute("""
            SELECT e.nom, SUM(c.kwh) AS total
            FROM consommation c
            JOIN equipements e ON c.equipement_id = e.id
            GROUP BY e.nom
            HAVING total > ?
        """, (seuil_kwh,))
        return cursor.fetchall()

    def consommation_par_source_graph(self):
        cursor = self.consommation_model.conn.cursor()
        cursor.execute("""
            SELECT s.nom, SUM(c.kwh) AS total
            FROM consommation c
            JOIN sources s ON c.source_id = s.id
            GROUP BY s.nom
        """)
        return cursor.fetchall()

    def total_cout(self):
        return self.consommation_model.total_cout()

    def historique_coupures(self):
        cursor = self.consommation_model.conn.cursor()
        cursor.execute("""
            SELECT debut, fin, duree
            FROM coupures
            ORDER BY debut DESC
        """)
        return cursor.fetchall()

    def enregistrer_coupure(self, debut, fin):
        duree = (fin - debut).total_seconds() / 3600
        cursor = self.consommation_model.conn.cursor()
        cursor.execute("""
            INSERT INTO coupures (debut, fin, duree)
            VALUES (?, ?, ?)
        """, (debut, fin, duree))
        self.consommation_model.conn.commit()

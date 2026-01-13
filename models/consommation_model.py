from models.database import Database
from datetime import datetime

class ConsommationModel:
    
    def __init__(self):
        self.db = Database()
        self.conn = self.db.conn

    def ajouter_consommation(self, equipement_id, source_id, kwh):
        cursor = self.conn.cursor()
        cursor.execute(
            """
            INSERT INTO consommation (equipement_id, source_id, kwh, date)
            VALUES (?, ?, ?, ?)
            """,
            (equipement_id, source_id, kwh, datetime.now())
        )
        self.conn.commit()

    def consommation_par_source(self):
        cursor = self.conn.cursor()
        cursor.execute("""
        SELECT s.nom, SUM(c.kwh) AS total
        FROM consommation c
        JOIN sources s ON c.source_id = s.id
        GROUP BY s.nom
        """)
        return cursor.fetchall()

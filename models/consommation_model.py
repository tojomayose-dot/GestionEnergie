from models.database import Database

class ConsommationModel:
    def __init__(self):
        self.db = Database()
        self.conn = self.db.conn

    def get_all(self):
        return self.conn.execute("""
            SELECT c.id, e.nom AS equipement, s.nom AS source, c.kwh, c.date
            FROM consommation c
            JOIN equipements e ON c.equipement_id = e.id
            JOIN sources s ON c.source_id = s.id
            ORDER BY c.date DESC
        """).fetchall()

    def create(self, equipement_id, source_id, kwh, date):
        self.conn.execute("""
            INSERT INTO consommation (equipement_id, source_id, kwh, date)
            VALUES (?, ?, ?, ?)
        """, (equipement_id, source_id, kwh, date))
        self.conn.commit()

    def delete(self, id_):
        self.conn.execute(
            "DELETE FROM consommation WHERE id=?", (id_,)
        )
        self.conn.commit()

    def total_cout(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT SUM(c.kwh * s.cout_kwh) AS total
            FROM consommation c
            JOIN sources s ON c.source_id = s.id
        """)
        result = cursor.fetchone()[0]
        return round(result, 2) if result else 0

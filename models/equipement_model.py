from models.database import Database

class EquipementModel:

    def __init__(self):
        self.db = Database()
        self.conn = self.db.conn

    def ajouter_equipement(self, nom, type_id, puissance_watt):
        cursor = self.conn.cursor()
        cursor.execute(
            """
            INSERT INTO equipements (nom, type_id, puissance_watt)
            VALUES (?, ?, ?)
            """,
            (nom, type_id, puissance_watt)
        )
        self.conn.commit()

    def lister_equipements(self):
        cursor = self.conn.cursor()
        cursor.execute("""
        SELECT e.id, e.nom AS type, e.puissance_watt
        FROM equipements e
        LEFT JOIN types_equipements t ON e.type_id = t.id
        """)
        return cursor.fetchall()
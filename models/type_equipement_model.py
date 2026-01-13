from models.database import Database

class TypeEquipementModel:
    
    def __init__(self):
        self.db = Database()
        self.conn = self.db.conn

    def ajouter_type(self, nom):
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO types_equipements (nom) VALUES (?)",
            (nom,)
        )
        self.conn.commit()
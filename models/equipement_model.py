from models.database import Database

class EquipementModel:
    def __init__(self):
        self.db = Database()
        self.conn = self.db.conn

    def get_all(self):
        return self.conn.execute(
            "SELECT * FROM equipements"
        ).fetchall()

    def create(self, nom):
        self.conn.execute(
            "INSERT INTO equipements (nom) VALUES (?)", (nom,)
        )
        self.conn.commit()

    def delete(self, id_):
        self.conn.execute(
            "DELETE FROM equipements WHERE id=?", (id_,)
        )
        self.conn.commit()

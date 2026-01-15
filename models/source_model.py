from models.database import Database

class SourceModel:
    def __init__(self):
        self.db = Database()
        self.conn = self.db.conn

    def get_all(self):
        return self.conn.execute(
            "SELECT * FROM sources"
        ).fetchall()

    def create(self, nom, cout_kwh):
        self.conn.execute(
            "INSERT INTO sources (nom, cout_kwh) VALUES (?, ?)",
            (nom, cout_kwh)
        )
        self.conn.commit()

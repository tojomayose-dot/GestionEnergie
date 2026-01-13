from models.database import Database

class SourceModel:
    
    def __init__(self):
        self.db = Database()
        self.conn = self.db.conn
    
    def ajouter_source(self, nom, cout_kwh):
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO sources (nom, cout_kwh) VALUES (?, ?)",
            (nom, cout_kwh)
        )
        self.conn.commit()

    def lister_sources(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM sources")
        return cursor.fetchall()
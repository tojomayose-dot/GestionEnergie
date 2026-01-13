import sqlite3

class Database:
    def __init__(self, db_name="energie.db"):
        self.db_name = db_name
        self.conn = None
        self.connect()
        self.create_tables()

    def connect(self):
        self.conn = sqlite3.connect(self.db_name)
        self.conn.row_factory = sqlite3.Row

    def create_tables(self):
        cursor = self.conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS sources (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT not NULL,
            cout_kwh REAL NOT NULL               
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS types_equipements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL               
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS equipements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            type_id INTEGER,
            puissance_watt REAL,
            FOREIGN KEY(type_id) REFERENCES types_equipements(id)
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS consommation (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            equipement_id INTEGER,
            source_id INTEGER,
            kwh REAL,
            date TIMESTAMP,
            FOREIGN KEY(equipement_id) REFERENCES equipements (id),
            FOREIGN KEY(source_id) REFERENCES sources(id) 
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS coupures (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            debut TIMESTAMP,
            fin TIMESTAMP,
            duree REAL
        )
        """)

        self.conn.commit()


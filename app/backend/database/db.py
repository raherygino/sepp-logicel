import sqlite3

class Database():

    def __init__(self):
        self.CONN = sqlite3.connect('database.db')
        self.CURSOR = self.CONN.cursor()

    def createTable(self, name:str, cols:list):
        query = "CREATE TABLE IF NOT EXISTS "+name
        query += " (id_"+name+" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, "
        for col in cols:
            query += col[0]+" "+col[1]+", "
        query += "created_at DATETIME)"
        self.CURSOR.execute(query)
        
    def query(self, query: str):
        self.CURSOR.execute(query)
        self.CONN.commit()


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

    def insert(self, table:str, cols: list):
        query = "INSERT INTO "+table+"("
        for col in cols:
            query += col[0]+" ,"
        query += "created_at) VALUES("

        for col in cols:
            query += "'"+str(col[2])+"', "
        query += "NULL)"
        self.query(query)
    
    def fetch(self, table:str, cols:list):
        query = "SELECT "
        for col in cols:
            query += col+","
        query = query[0:len(query)-1]
        query += " FROM "+table
        self.CURSOR.execute(query)
        return self.CURSOR.fetchall()
    
    def ff(self):
        return list(map(lambda x: x[0], self.CURSOR.description))



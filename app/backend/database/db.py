import sqlite3

class Database():

    def __init__(self):
        self.CONN = sqlite3.connect('database.db')
        self.CURSOR = self.CONN.cursor()

    class table:
        def __init__(self, name:str):
            self.db = Database()
            self.name = name
            self.connect = self.db.CONN
            self.cursor = self.db.CURSOR

        def create(self, cols):
            query = "CREATE TABLE IF NOT EXISTS "+self.name
            query += " (id_"+self.name+" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, "
            for col in cols:
                query += col+" TEXT, "
            query += "created_at DATETIME)"
            self.cursor.execute(query)

        def store(self, cVal):
            query = "INSERT INTO "+self.name+"("
            for col in cVal:
                query += col[0]+" ,"
            query += "created_at) VALUES("
            for col in cVal:
                query += "'"+str(col[1])+"', "
            query += "NULL)"
            self.db.query(query)

        def all(self, cols):
            query = "SELECT "
            for col in cols:
                query += col+","
            query = query[0:len(query)-1]
            query += " FROM "+self.name
            self.db.CURSOR.execute(query)
            return self.db.CURSOR.fetchall()
        
        def get(self, id, cols):
            query = "SELECT "
            for col in cols:
                query += col+","
            query = query[0:len(query)-1]
            query += f" FROM {self.name} WHERE id_{self.name} = '{id}'"

            self.cursor.execute(query)
            return self.cursor.fetchone()
    
        def search(self, cols:list, condition:str):
            query = "SELECT "
            for col in cols:
                query += col+","
            query = query[0:len(query)-1]
            query += " FROM "+self.name+ " WHERE "+ condition
            self.cursor.execute(query)
            return self.cursor.fetchall()
        
        def delete(self, id):
            self.cursor.execute(f"DELETE FROM {self.name} WHERE id_{self.name} = '{id}'")
            self.connect.commit()




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
    
    def search(self, table:str, cols:list, condition:str):
        query = "SELECT "
        for col in cols:
            query += col+","
        query = query[0:len(query)-1]
        query += " FROM "+table+ " WHERE "+ condition
        self.CURSOR.execute(query)
        return self.CURSOR.fetchall()

    
    def fetchById(self, table:str, id, cols:list):
        query = "SELECT "
        for col in cols:
            query += col+","
        query = query[0:len(query)-1]
        query += f" FROM {table} WHERE id_{table} = '{id}'"

        self.CURSOR.execute(query)
        return self.CURSOR.fetchone()
    
    def delete(self, table:str, id):
        self.CURSOR.execute(f"DELETE FROM {table} WHERE id_{table} = '{id}'")
        self.CONN.commit()



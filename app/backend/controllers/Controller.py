from ..database.db import Database as DB

class Controller():
    
    def __init__(self, name, cols):
        db = DB()
        db.createTable(name, cols)
        self.CURSOR = db.CURSOR
        self.CONN = db.CONN
        self.TABLE_NAME = name
        self.COLS = cols

    def query(self, query:str):
        self.CURSOR.execute(query)
        self.CONN.commit()
        
    def insert(self, values):
        query = "INSERT INTO "+self.TABLE_NAME+"("

        for col in self.COLS:
            query += col[0]+", "
        query += "created_at) VALUES ("
        
        for val in values:
            query += "'"+val+"', "
        query += "'')"

        self.query(query)
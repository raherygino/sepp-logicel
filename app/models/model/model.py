from ..db.database import Database
from ..entity import Entity
import dataclasses

class Model:
    def __init__(self, table: str, entity:Entity):
        self.TABLE = table
        self.database = Database()
        self.conn = self.database.connect()
        self.entity = entity
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        query = f"CREATE TABLE IF NOT EXISTS {self.TABLE}("
        
        for field in dataclasses.fields(self.entity):
            fieldType = str(field.type)
            if (fieldType.find('str') != -1):
                fieldType = "TEXT"
            else:
                if (field.name == "id"):
                    fieldType = "INTEGER PRIMARY KEY"
                else:
                    fieldType = "INTEGER"
            query += f"{field.name} {fieldType}, "

        query += "updated_at DATETIME, created_at DATETIME)"
        cursor.execute(query)
        self.conn.commit()
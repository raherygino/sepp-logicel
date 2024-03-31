from ..db import Database
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
    
    def fetch_all(self, **kwargs):
        query = f'SELECT * FROM {self.TABLE}'
        if "order" in kwargs.keys():
            query += f' ORDER BY {kwargs.get('order')}'
        cursor = self.conn.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        listItems = []
        listItems.clear()

        for val in data:
            nVal = self.entity.copy()
            fieldsEntity = dataclasses.fields(nVal)
            for i, field in enumerate(fieldsEntity):
                nVal.set(field.name, val[i])
            listItems.append(nVal)
        return listItems
    
    def create(self, entity: Entity):
        fieldsEntity = dataclasses.fields(entity)
        qm = ','.join([f'?' for field in fieldsEntity[1:]])
        values = [f'{entity.get(field.name)}' for field in fieldsEntity[1:]]
        fields = ','.join([f'{field.name}' for field in fieldsEntity[1:]])
        sql = f"INSERT INTO {self.TABLE}({fields}) VALUES ({qm})"
        cursor = self.conn.cursor()
        cursor.execute(sql, values)
        self.conn.commit()
    
    def delete(self,**kwargs):
        sql = f'DELETE FROM {self.TABLE} WHERE '
        conditions = ' AND '.join([f'{key}="{kwargs.get(key)}"' for key in kwargs.keys()])
        sql += conditions
        cursor = self.conn.cursor()
        cursor.execute(sql)
        self.conn.commit()
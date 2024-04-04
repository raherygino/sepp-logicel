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
        return self.resultToEntity(cursor.fetchall())
    
    def fetch_by_condition(self, **kwargs):
        query = f'SELECT * FROM {self.TABLE}'
        if len(kwargs) != 0:
            cond = ' AND '.join([f'{key}="{kwargs.get(key)}"' for key in kwargs.keys()])
            query += " WHERE "+cond
        cursor = self.conn.cursor()
        cursor.execute(query)
        return self.resultToEntity(cursor.fetchall())
    
    def max_col(self, col, **kwargs) -> int:
        query = f'SELECT max({col}) as maxim FROM {self.TABLE}'
        cond = ""
        if len(kwargs) != 0:
            cond = ' AND '.join([f'{key}="{kwargs.get(key)}"' for key in kwargs.keys()])
            query += f" WHERE {cond}"
        
        cursor = self.conn.cursor()
        cursor.execute(query)
        data = cursor.fetchall()[0][0]
        return data if data != None else 0
    
    def create(self, entity: Entity):
        fieldsEntity = dataclasses.fields(entity)
        qm = ','.join([f'?' for field in fieldsEntity[1:]])
        values = [f'{entity.get(field.name)}' for field in fieldsEntity[1:]]
        fields = ','.join([f'{field.name}' for field in fieldsEntity[1:]])
        sql = f"INSERT INTO {self.TABLE}({fields}) VALUES ({qm})"
        cursor = self.conn.cursor()
        cursor.execute(sql, values)
        self.conn.commit()
    
    def create_multiple(self, listData: list):
        cursor = self.conn.cursor()
        for entity in listData:
            fieldsEntity = dataclasses.fields(entity)
            qm = ','.join([f'?' for field in fieldsEntity[1:]])
            values = [f'{entity.get(field.name)}' for field in fieldsEntity[1:]]
            fields = ','.join([f'{field.name}' for field in fieldsEntity[1:]])
            sql = f"INSERT INTO {self.TABLE}({fields}) VALUES ({qm})"
            cursor.execute(sql, values)
        self.conn.commit()
        
    def update_item(self, item_id, **fields):
        cursor = self.conn.cursor()
        id_col = dataclasses.fields(self.entity)[0].name
        
        sql = f"UPDATE {self.TABLE} SET"

        for i, key in enumerate(fields.keys()):
            if i == 0:
                sql += f" {key} = \"{fields.get(key).replace("\"", "")}\" "
            else:
                sql += f", {key} = \"{fields.get(key).replace("\"", "")}\" "
        sql += f"WHERE {id_col}={item_id}"
        cursor.execute(sql)
        self.conn.commit()
    
    def delete(self,**kwargs):
        sql = f'DELETE FROM {self.TABLE} WHERE '
        conditions = ' AND '.join([f'{key}="{kwargs.get(key)}"' for key in kwargs.keys()])
        sql += conditions
        cursor = self.conn.cursor()
        cursor.execute(sql)
        self.conn.commit()
        
    def resultToEntity(self, data):
        listItems = []
        listItems.clear()
        for val in data:
            nVal = self.entity.copy()
            fieldsEntity = dataclasses.fields(nVal)
            for i, field in enumerate(fieldsEntity):
                nVal.set(field.name, val[i])
            listItems.append(nVal)
        return listItems
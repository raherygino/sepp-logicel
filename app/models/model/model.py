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
        is_kwargs = len(kwargs) != 0
        keywords = ["order", "group"]
        keys = []
        query = f'SELECT * FROM {self.TABLE}'
        if is_kwargs:
            cond = ""
            order = ""
            orders = []
            for key in kwargs.keys():
                if key not in keywords:
                    cond += f'AND {key}="{kwargs.get(key)}" '
                    keys.append(key)
                else:
                    if key == "order":
                        order += f" ORDER BY {kwargs.get(key)} DESC"
                    elif key == "group":
                        order += f" GROUP BY {kwargs.get(key)}"
                    orders.append(key)
            query += " WHERE "+cond[4:] if "order" not in keys and "group" not in keys else ""
            query = query.replace("WHERE","") if query.find("\"") == -1 else query
            query += order if "order" in orders or "group" in orders else ""
        cursor = self.conn.cursor()
        cursor.execute(query)
        return self.resultToEntity(cursor.fetchall())
    
    def search(self,prefix=None, id=None, **kwargs):
        sql = f'SELECT * FROM {self.TABLE} WHERE '
        if prefix != None:
            sql += f"{prefix}_id='{id}' AND "
        condition = ' OR '.join([f'{key} LIKE "%{kwargs.get(key).replace("\"", "")}%"' for key in kwargs.keys()])
        sql += condition
        cursor = self.conn.cursor()
        cursor.execute(sql)
        return self.resultToEntity(cursor.fetchall())
      
    def count(self, **kwargs):
        query = f"SELECT count(id) as cnt FROM {self.TABLE}"
        cond = ""
        if len(kwargs) != 0:
            cond = ' AND '.join([f'{key}="{kwargs.get(key)}"' for key in kwargs.keys()])
            query += f" WHERE {cond}"
        cursor = self.conn.cursor()
        cursor.execute(query)
        data = cursor.fetchall()[0][0]
        return data if data != None else 0
    
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
from ..db.database import Database
from ..entity.base_entity import Entity
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


    def fetch_all_items(self, **kwargs):
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
    
    def fetch_items_by_id(self, id_item,**kwargs):
        id_col = dataclasses.fields(self.entity)[1].name
        sql = f'SELECT * FROM {self.TABLE} WHERE {id_col} = "{id_item}"'
        if "order" in kwargs.keys():
            sql += f' ORDER BY {kwargs.get('order')}'
        if "group_by" in kwargs.keys():
            sql += f' GROUP BY {kwargs.get('group_by')}'
        cursor = self.conn.cursor()
        cursor.execute(sql)
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
    
    def fetch_items_by_cond(self, **kwargs):
        col = ""
        for key in kwargs.keys():
            col = key
        cursor = self.conn.cursor()
        cursor.execute(f'SELECT * FROM {self.TABLE} WHERE {col} LIKE "%{kwargs.get(col)}%"')
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
    
    def search(self, **kwargs):
        
        sql = f'SELECT * FROM {self.TABLE} WHERE '
        condition = ' OR '.join([f'{key} LIKE "%{kwargs.get(key)}%"' for key in kwargs.keys()])
        sql += condition
        cursor = self.conn.cursor()
        cursor.execute(sql)
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
    
    def search_with_id(self, id, **kwargs):

        id_col = dataclasses.fields(self.entity)[1].name
        sql = f'SELECT * FROM {self.TABLE} WHERE {id_col} = "{id}" AND '
        condition = ' OR '.join([f'{key} LIKE "%{kwargs.get(key)}%"' for key in kwargs.keys()])
        sql += condition
        cursor = self.conn.cursor()
        cursor.execute(sql)
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

    def fetch_item_by_id(self, id_item):
        id_col = dataclasses.fields(self.entity)[0].name
        cursor = self.conn.cursor()
        cursor.execute(f'SELECT * FROM {self.TABLE} WHERE {id_col} = "{id_item}"')
        data = cursor.fetchall()
        listItems = []
        listItems.clear()

        for val in data:
            nVal = self.entity.copy()
            fieldsEntity = dataclasses.fields(nVal)
            for i, field in enumerate(fieldsEntity):
                nVal.set(field.name, val[i])
            listItems.append(nVal)
        return listItems[0] if len(listItems) != 0 else None

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
                sql += f" {key} = \"{fields.get(key)}\" "
            else:
                sql += f", {key} = \"{fields.get(key)}\" "
        sql += f"WHERE {id_col}={item_id}"
        cursor.execute(sql)
        self.conn.commit()

    def delete_item(self, item_id):
        
        id_col = dataclasses.fields(self.entity)[0].name
        cursor = self.conn.cursor()
        cursor.execute(f'DELETE FROM {self.TABLE} WHERE {id_col}=?', (item_id,))
        self.conn.commit()

    def delete_with_cond(self, **kwargs):
        col = ""
        for key in kwargs.keys():
            col = key
        
        cursor = self.conn.cursor()
        cursor.execute(f'DELETE FROM {self.TABLE} WHERE {col}=?', (kwargs.get(col),))
        self.conn.commit()

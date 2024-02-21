from ..db.database import Database
from ..entity.base_entity import Entity
import dataclasses
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import sqlite3

class WorkerThread(QThread):
    update_progress = pyqtSignal(int)
    finished = pyqtSignal()

    def __init__(self, conn, sql, parent=None):
        super(WorkerThread, self).__init__(parent)
        self.conn = conn
        self.sql = sql

    def run(self):
        # Connect to SQLite database
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        

        # Fetch data from SQLite database
        cursor.execute(self.sql)
        data = cursor.fetchall()
        total_rows = len(data)

        # Update progress bar and emit signals
        for i, row in enumerate(data):
            # Simulate processing delay
            self.msleep(1)
            progress = int((i + 1) / total_rows * 100)
            self.update_progress.emit(progress)

        self.conn.close()
        self.finished.emit()

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

    def test_thread(self) -> WorkerThread:
        return WorkerThread(self.conn, f"SELECT * FROM {self.TABLE}")

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
    
    def fetch_items_by_col(self, id, **kwargs):
        id_col = dataclasses.fields(self.entity)[1].name
        listItems = []
        if len(kwargs) != 0:
            cols = ' AND '.join([f'{key}="{kwargs.get(key)}"' for key in kwargs])
            sql = f'SELECT * FROM {self.TABLE} WHERE {id_col} = "{id}" AND '
            sql += cols
            cursor = self.conn.cursor()
            cursor.execute(sql)
            data = cursor.fetchall()
            
            for val in data:
                nVal = self.entity.copy()
                fieldsEntity = dataclasses.fields(nVal)
                for i, field in enumerate(fieldsEntity):
                    nVal.set(field.name, val[i])
                listItems.append(nVal)
            cursor.close()
        return listItems
    
    def search(self, **kwargs):
        
        sql = f'SELECT * FROM {self.TABLE} WHERE '
        condition = ' OR '.join([f'{key} LIKE "%{kwargs.get(key).replace("\"", "")}%"' for key in kwargs.keys()])
        sql += condition
        print(sql)
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
    
    def count_by(self,**kwargs):
        count = 0
        if len(kwargs) != 0:
            key = ''.join([f'{key}' for key in kwargs])
            sql = f'SELECT * FROM {self.TABLE} WHERE {key} = "{kwargs.get(key)}"'
            cursor = self.conn.cursor()
            cursor.execute(sql)
            count = len(cursor.fetchall())
            cursor.close()
        return count
    
    def count_by_with_id(self,id, **kwargs):
        id_col = dataclasses.fields(self.entity)[1].name
        count = 0
        if len(kwargs) != 0:
            cols = ' AND '.join([f'{key}="{kwargs.get(key)}"' for key in kwargs])
            sql = f'SELECT * FROM {self.TABLE} WHERE {id_col} = "{id}" AND '
            sql += cols
            cursor = self.conn.cursor()
            cursor.execute(sql)
            count = len(cursor.fetchall())
            cursor.close()
        return count
    
    def sum_by_with_id(self, id,col, **kwargs):
        id_col = dataclasses.fields(self.entity)[1].name
        sumOfCol = 0
        sql = f'SELECT sum({col}) as cnt, {id_col} FROM {self.TABLE} WHERE {id_col} = "{id}"'
        if len(kwargs) != 0:
            key = ''.join([f'{key}' for key in kwargs])
            sql += f' AND {key}="{kwargs.get(key)}"'
        cursor = self.conn.cursor()
        cursor.execute(sql)
        sumOfCol = cursor.fetchall()[0][0]
        cursor.close()
        return sumOfCol if sumOfCol != None else ""
            
    def search_with_id(self, id, **kwargs):
        id_col = dataclasses.fields(self.entity)[1].name
        sql = f'SELECT * FROM {self.TABLE} WHERE '
        condition = ' OR '.join([f'({id_col} = "{id}" AND {key} LIKE "%{kwargs.get(key).replace("\"", "")}%")' for key in kwargs.keys()])
        sql += condition
        cursor = self.conn.cursor()
        cursor.execute(sql)
        data = cursor.fetchall()
        cursor.close()
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

    def fetch_item_by_cols(self, **kwargs):
        cursor = self.conn.cursor()
        sql = f'SELECT * FROM {self.TABLE} WHERE '
        sql += ' AND '.join([f'{key}="{kwargs.get(key)}"' for key in kwargs.keys()])
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
                sql += f" {key} = \"{fields.get(key).replace("\"", "")}\" "
            else:
                sql += f", {key} = \"{fields.get(key).replace("\"", "")}\" "
        sql += f"WHERE {id_col}={item_id}"
        cursor.execute(sql)
        self.conn.commit()

    def delete_item(self, item_id):
        
        id_col = dataclasses.fields(self.entity)[0].name
        cursor = self.conn.cursor()
        cursor.execute(f'DELETE FROM {self.TABLE} WHERE {id_col}=?', (item_id,))
        self.conn.commit()

    def delete_by(self,**kwargs):
        
        sql = f'DELETE FROM {self.TABLE} WHERE '
        conditions = ' AND '.join([f'{key}="{kwargs.get(key)}"' for key in kwargs.keys()])
        sql += conditions
        cursor = self.conn.cursor()
        cursor.execute(sql)
        self.conn.commit()

    def delete_with_cond(self, **kwargs):
        col = ""
        for key in kwargs.keys():
            col = key
        
        cursor = self.conn.cursor()
        cursor.execute(f'DELETE FROM {self.TABLE} WHERE {col}=?', (kwargs.get(col),))
        self.conn.commit()

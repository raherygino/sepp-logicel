# coding:utf-8
from typing import List

from PyQt5.QtSql import QSqlDatabase, QSqlRecord

from ..entity import Entity, EntityFactory
from .sql_query import SqlQuery
import dataclasses


def finishQuery(func):
    """ Finish sql query to unlock database """

    def wrapper(dao, *args, **kwargs):
        result = func(dao, *args, **kwargs)
        dao.query.finish()
        return result

    return wrapper

class DaoBase:
    """ Database access operation abstract class """

    table = ''
    fields = ['id']

    def __init__(self, db: QSqlDatabase = None):
        self.setDatabase(db)

    def createTable(self, obj):
        """ create table """
        query = f"CREATE TABLE IF NOT EXISTS {self.table}("
        query += f"id_{self.table} INTEGER PRIMARY KEY, "
        
        for field in dataclasses.fields(obj):
            fieldType = str(field.type)
            if (fieldType.find('str') != -1):
                fieldType = "TEXT"
            else:
                fieldType = "INTEGER"
            query += f"{field.name} {fieldType}, "

        query += "updated_at, created_at DATETIME)"
        return self.query.exec(query)

    @finishQuery
    def create(self, entity: Entity):
        values = ','.join([f'"{entity.get(i)}"' for i in self.fields])
        fields = ','.join([f'{i}' for i in self.fields])
        sql = f"INSERT INTO {self.table}({fields}) VALUES ({values})"
        self.query.prepare(sql)
        self.bindEntityToQuery(entity)
        return self.query.exec()
   
    @finishQuery
    def update(self, id:int, entity:Entity) -> bool:
    
        fields = ','.join([f'{field} = \'{entity.get(field)}\'' for field in self.fields])
        sql = f"UPDATE {self.table} SET {fields} WHERE id_{self.table} = '{id}'"
        return self.query.exec(sql)
   
    @finishQuery
    def deleteById(self, id) -> bool:
        """ delete a record """
        sql = f"DELETE FROM {self.table} WHERE id_{self.table} = ?"
        self.query.prepare(sql)
        self.query.addBindValue(id)
        return self.query.exec()

    def listAll(self) -> List[Entity]:
        """ query all records """
        sql = f"SELECT * FROM {self.table}"
        
        
        if not self.query.exec(sql):
            return []

        return self.iterRecords()
    
    def search(self, query) -> List[Entity]:
        """search query records """

        condition = ' OR '.join([f'{field} LIKE \'%{query}%\' ' for field in self.fields])
        sql = f"SELECT * FROM {self.table} WHERE {condition}"
        
        if not self.query.exec(sql):
            return []
        return self.iterRecords()

    def listByFields(self, field: str, values: list):
        """ query the records of field values in the list """
        #if field not in self.fields & field not id:
        #    raise ValueError(f"field name `{field}` is illegal")

        if not values:
            return []

        placeHolders = ','.join(['?']*len(values))
        sql = f"SELECT * FROM {self.table} WHERE {field} IN ({placeHolders})"
        self.query.prepare(sql)

        for value in values:
            self.query.addBindValue(value)

        if not self.query.exec():
            return []

        return self.iterRecords()

    def listByIds(self, ids: list) -> any:
        """ query the records of the primary key value in the list """
        return self.listByFields(f"id_{self.table}", ids)
    
    def _prepareSelectBy(self, condition: dict):
        """ prepare sql select statement

        Parameters
        ----------
        table: str
            table name

        condition: dict
            query condition
        """
        if not condition:
            raise ValueError("At least one condition must be passed in")

        commands = ['orderBy', 'limit', 'desc']
        sql = f"SELECT * FROM {self.table}"

        keys = [i for i in condition.keys() if i not in commands]
        if keys:
            where = [f'{k} = ?' for k in keys]
            sql += f" WHERE  {' AND '.join(where)}"

        if 'orderBy' in condition:
            sql += f" ORDER BY {condition['orderBy']}"
            if 'desc' in condition and condition['desc']:
                sql += ' DESC'

        if 'limit' in condition:
            sql += f" LIMIT {condition['limit']}"

        self.query.prepare(sql)
        for k in keys:
            self.query.addBindValue(condition[k])

    def _prepareSelectLike(self, condition: dict):
        """ prepare sql fuzzy select statement

        Parameters
        ----------
        table: str
            table name

        condition: dict
            query condition
        """
        if not condition:
            raise ValueError("At least one condition must be passed in")

        placeholders = [f"{k} like ?" for k in condition.keys()]
        sql = f"SELECT * FROM {self.table} WHERE {' OR '.join(placeholders)}"
        self.query.prepare(sql)
        for v in condition.values():
            self.query.addBindValue(f'%{v}%')

    @finishQuery
    def iterRecords(self) -> List[Entity]:
        """ iterate over all queried records """
        entities = []

        while self.query.next():
            entity = self.loadFromRecord(self.query.record())
            entities.append(entity)

        return entities

    def clearTable(self):
        """ clear all data from table """
        return self.query.exec(f"DELETE FROM {self.table}")

    @classmethod
    def loadFromRecord(cls, record: QSqlRecord) -> Entity:
        """ create an entity instance from a record """
        entity = EntityFactory.create(cls.table)

        for i in range(record.count()):
            field = record.fieldName(i)
            entity[field] = record.value(i)

        return entity

    def adjustText(self, text: str):
        """ handling single quotation marks in strings """
        return text.replace("'", "''")

    def bindEntityToQuery(self, entity: Entity):
        """ bind the value of entity to query object """
        for field in self.fields:
            value = entity[field]
            self.query.bindValue(f':{field}', value)

    def setDatabase(self, db: QSqlDatabase):
        """ use the specified database """
        self.connectionName = db.connectionName() if db else ''
        self.query = SqlQuery(db) if db else SqlQuery()
        self.query.setForwardOnly(True)

    def getDatabase(self):
        """ get connected database """
        if self.connectionName:
            return QSqlDatabase.database(self.connectionName)

        return QSqlDatabase.database()

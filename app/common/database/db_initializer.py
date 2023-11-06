# coding:utf-8
from PyQt5.QtSql import QSqlDatabase
from PyQt5.QtWidgets import qApp

from .service.student_service import StudentService

class DBInitializer:
    """ Database initializer """

    CONNECTION_NAME = "main"
    CACHE_FILE = str("student.db")

    @classmethod
    def init(cls):
        """ Initialize database """
        db = QSqlDatabase.addDatabase('QSQLITE', cls.CONNECTION_NAME)
        db.setDatabaseName(cls.CACHE_FILE)
        if not db.open():
            cls.logger.error("Database connection failed")
            qApp.exit()

        StudentService(db).createTable()
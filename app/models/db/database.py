import sqlite3

class Database():
    def connect(self):
        return sqlite3.connect("database.db")   
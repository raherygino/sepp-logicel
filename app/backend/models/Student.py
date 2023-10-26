from ..database.db import Database as DB

class Student():

    def __init__(self, 
                 lastname:str, 
                 firstname:str, 
                 genre:str, 
                 height:int,
                 weight:int,
                 birthday:str, 
                 birthplace:str, 
                 phone:str, 
                 address:str, 
                 level:str,
                 company:int, 
                 section:int, 
                 number:int):
        self.db = DB()
        self.data = {}
        self.cols = []
        for name in dir():
            if not name.startswith("__") and name != "self":
                myvalue = eval(name)
                self.data[name] = myvalue
                typeVar = type(myvalue)
                type_var = str(typeVar).split("\'")[1]
                typVar = "TEXT"
                if type_var == "int":
                    typVar = "INTEGER"
                self.cols.append([name, typVar, self.data[name]])

    def getData(self):
        return self.data
    
    def create(self):
        self.db.createTable("student", self.cols)
        self.db.insert("student", self.cols)


    def fetch(self, cols):
        return self.db.fetch("student", cols)
    
    def column(self):
        return self.db.ff()


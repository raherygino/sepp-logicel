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
    
    def initTable(self):
        self.db.createTable("student", self.cols)

    def create(self):
        self.initTable()
        self.db.insert("student", self.cols)

    def seed(self, obj:dict):
        cols = [
            ["lastname", "TEXT", obj.get("lastname")],
            ["firstname", "TEXT", obj.get("firstname")],
            ["genre", "TEXT", obj.get("genre")],
            ["height", "TEXT", obj.get("height")],
            ["weight", "TEXT", obj.get("weight")],
            ["birthday", "TEXT", obj.get("birthday")],
            ["birthplace", "TEXT", obj.get("birthplace")],
            ["phone", "TEXT", obj.get("phone")],
            ["level", "TEXT", obj.get("level")],
            ["company", "TEXT", obj.get("company")],
            ["section", "TEXT", obj.get("section")],
            ["number", "TEXT", obj.get("number")]
        ]
        return cols
    
    def seeds(self, lenght):
        lastname = ["RAKOTO", "RABE", "RANDRIA", "RASOA", "ANDRIANINA", "RAKOTOMALALA", "RANAIVOSON",
                    "RAHERY", "RANDRIANARIVO", "NARISON", "MAHERINIANA", "HERINIAINA", "RASOLOMALALA"
                    "SOLOMALALA", "RAKOTOBE", "RAVAO"]
        firstname = ["Jean Yves", "Michel", "Michael", "Georges", "Grégoire", "Lianah", "Dina", "Malala",
                     "Prisca", "Tiana", "Mahefa", "Haigotiana", "Malalatiana", "Faramalala", "Rado", 
                     "Jean Jacques"]
    

    def fetch(self, cols):
        return self.db.fetch("student", cols)
    
    def fetchById(self, id):


        data = self.db.fetchById("student", id, [
            "firstname", "lastname", "genre",
            "height", "weight", "birthday","birthplace", "phone", "address",
            "level", "company", "section", "number"
        ])

        return {
            "id": id,
            "firstname" : data[0],
            "lastname": data[1],
            "genre": data[2],
            "height": data[3],
            "weight": data[4],
            "birthday": data[5],
            "birthplace": data[6],
            "phone": data[7],
            "address": data[8],
            "level": data[9],
            "company": data[10],
            "section": data[11],
            "number": data[12]
        }
        
    def delete(self, id):
        self.db.delete("student", id)
    
    def column(self):
        return self.db.ff()


from .Model import Model
from .keys import *
import random

class Student(Model):
    
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
        
        self.tableName = "student"
        self.lastname = lastname
        self.firstname = firstname
        self.genre = genre
        self.height = height
        self.weight = weight
        self.birthday = birthday
        self.birthplace = birthplace
        self.phone = phone
        self.address = address
        self.level = level
        self.company = company
        self.section = section
        self.number = number
        if company != None:
            self.number = f"{company[0]+section[0]+str(number)}"

        super().__init__(self.tableName,dir())
    
    def create(self):
        vals = []
        for val in self.cols:
            vals.append(eval(f"self.{val}"))
        data = self.contentValues(vals)
        self.db.table(self.tableName).store(data)

    def get(self, id):

        data = self.db.table(self.tableName).get(id, STUDENT_COLS)

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
        company = ["1ère", "2ème", "3ème"]
        section = ["1ère", "2ème", "3ème", "4ème", "5ème", "6ème", "7ème", "8ème"]

        
        for i in range(0, lenght - 1):
            rand_1 = random.randint(0,len(lastname) -1 )
            rand_2 = random.randint(0, len(firstname) - 1)
            rand_3 = random.randint(0, len(company) - 1)
            rand_4 = random.randint(0, len(section) - 1)
            lastName = lastname[rand_1]
            firstName = firstname[rand_2]
            comp = company[rand_3]
            sect = section[rand_4]
            number = random.randint(1,40)
            compInt = int(comp[0])
            sectInt = int(sect[0])
            level = "Eleve Agent de Police"
            if compInt == 1 and sectInt == 1:
                level = "Eleve Inspecteur de Police"
            if compInt == 2 and sectInt == 1:
                level = "Eleve Inspecteur de Police"
            if compInt == 3 and sectInt == 1:
                level = "Eleve Inspecteur de Police"

            date_naissance = f"{random.randint(1, 28)}-{random.randint(1,12)}-19{random.randint(90,99)}"
            lieu_naissance = "-"
            student = Student(lastName,
                              firstName, 
                              ['M', 'L'][random.randint(0,1)],
                              random.randint(165, 190), random.randint(60, 90), date_naissance,
                              lieu_naissance, f"03{random.randint(2,4)} {random.randint(11, 99)} {random.randint(111, 999)} {random.randint(11, 99)}",
                              "-", level, comp, sect, number)
            student.create()
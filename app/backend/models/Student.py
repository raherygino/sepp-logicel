from .Model import Model


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

        super().__init__(self.tableName,dir())
    
    def create(self):
        vals = []
        for val in self.cols:
            vals.append(eval(f"self.{val}"))
        data = self.contentValues(vals)
        self.db.table(self.tableName).store(data)

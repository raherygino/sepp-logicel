
class Student():

    def __init__(self, lastname:str, firstname:str, phone:str, address:str, level:str, company:int, section:int, number:int):
    
        self.data = {}
        for name in dir():
            if not name.startswith("__") and name != "self":
                myvalue = eval(name)
                self.data[name] = myvalue
        
    def getData(self):
        return self.data

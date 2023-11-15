

class User:
    
    def __init__(self, **kwargs):
        self.dict = kwargs

    def createTable(self):
        for key in self.dict:
            print(key)
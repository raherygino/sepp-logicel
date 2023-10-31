from ..models.Example import Example
from ..database.db import Database

class ExampleController:

    def __init__(self):
        self.db = Database()
        self.example = Example(None, None)

    def store(self, example:Example):
        example.create()

    def fetch(self):
        return self.example.all(["name", "age"])
    
    def show(self, id):
        return self.example.get(id)
    
    def search(self, q):
        return self.example.search(["name", "age"], q)
    
    def delete(self, id):
        self.example.delete(id)
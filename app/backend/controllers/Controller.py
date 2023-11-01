from ..database.db import Database as DB

class Controller():
    
    def __init__(self, model, cols):
        self.model = model
        self.cols = cols

    def store(self, model):
        model.create()

    def fetch(self):
        return self.model.all(self.cols)
    
    def show(self, id):
        return self.model.get(id)
    
    def search(self, q):
        return self.model.search(self.cols, q)
    
    def delete(self, id):
        self.model.delete(id)

    def get(self, id):
        return self.model.get(id)
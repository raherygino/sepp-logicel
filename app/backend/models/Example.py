from .Model import Model


class Example(Model):
    

    def __init__(self, name, age):
        self.tableName = "example"
        self.name = name
        self.age = age
        super().__init__(self.tableName,dir())
    
    def create(self):
        vals = []
        for val in self.cols:
            vals.append(eval(f"self.{val}"))
        data = self.contentValues(vals)
        self.db.table(self.tableName).store(data)

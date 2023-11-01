from .Model import Model


class Movement(Model):
    
    def __init__(self, idStudent, startDate, motif, day):
        self.tableName = "mouvement"
        self.idStudent = idStudent
        self.startDate = startDate
        self.motif = motif
        self.day = day
        super().__init__(self.tableName,dir())

        
    def create(self):
        vals = []
        for val in self.cols:
            vals.append(eval(f"self.{val}"))
        data = self.contentValues(vals)
        self.db.table(self.tableName).store(data)
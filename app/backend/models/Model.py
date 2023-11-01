from ..database.db import Database as DB

class Model(dict):

    def __init__(self, tableName, dir):
        self.db = DB()
        self.cols = []
        self.tableName = tableName

        for name in dir:
            if not name.startswith("__") and name != "self":
                self.cols.append(name)
                
        self.db.table(tableName).create(self.cols)
    
    def contentValues(self, values):
        data = []
        for i, value in enumerate(values):
            data.append([self.cols[i], value])
        return data
    
    def all(self, cols):
        return self.db.table(self.tableName).all(cols)
        
    def get(self, id):
        return self.db.table(self.tableName).get(id, self.cols)
    
    def getByCol(self, col, val, cols):
        return self.db.table(self.tableName).getByCol(col, val, cols)
    
    def sumCol(self, id):
        return self.db.table(self.tableName).sumCol(col="day", col_cond = "idStudent", val_cond=id)
    
    def search(self,cols, query:str):
        cond = ""
        for col in cols:
            cond += f"{col} like '%{query}%' OR "
        cond = cond[0:len(cond) - 4]
        return self.db.table(self.tableName).search(cols, cond)

    def delete(self, id):
        self.db.table(self.tableName).delete(id)
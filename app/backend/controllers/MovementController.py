from .Controller import Controller
from ..models.Movement import Movement
from ..models.keys import *

class MovementController(Controller):

    def __init__(self):
        self.movement = Movement(None, None, None, None)
        self.label = STUDENT_TABLE_LABEL
        self.cols = ["idStudent", "startDate", "motif", "day"]
        super().__init__(self.movement, self.cols)

    def getByIdStudent(self, id):
        return self.movement.getByCol("idStudent", id, ["startDate", "motif", "day"])
    
    def sumOfDay(self, id):
        return self.movement.sumCol(id)



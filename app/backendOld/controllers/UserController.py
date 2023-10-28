from .Controller import Controller
from ..models.User import User

class UserController(Controller):

    def __init__(self, user: User):
        self.user = user
        table = user.table
        cols = user.cols
        super().__init__(table, cols)
        
    def create(self):
        super().insert(self.user.data())
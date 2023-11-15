from ..models import *

class UserController:

    def __init__(self):
        self.user = User(
            firstname = None,
            lastname = None,
            Age = None
        )
        self.user.createTable()

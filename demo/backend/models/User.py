

class User(object):
    firstname = ""
    lastname = ""
    username = ""
    email = ""
    phone = ""

    def __init__(self, firstname:str, lastname:str, username:str, email:str, phone:str):
        self.firstname = firstname
        self.lastname = lastname
        self.username = username
        self.email = email
        self.phone = phone
        self.table = "users"
        self.cols = [
            ['firstname', 'TEXT'],
            ['lastname', 'TEXT'],
            ['username', 'TEXT'],
            ['email', 'TEXT'],
            ['phone', 'TEXT']]
    
    def data(self):
        return [self.firstname, self.lastname, self.username, self.email, self.phone]
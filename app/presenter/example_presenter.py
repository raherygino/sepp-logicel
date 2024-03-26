from ..models import ExampleModel
from ..view.utils import ExampleInterface

class ExamplePresenter:
    
    def __init__(self, view:ExampleInterface, model: ExampleModel):
        self.view = view
        self.model = model
        #self.__actions()
        
    def __actions(self):
        print('hello')
from ..common.functions import Function

class ComportementPresenter:

    def __init__(self, view, model, parentPresenter):
        self.view = view
        self.model = model
        self.parentPresenter = parentPresenter
        self.func = Function()
        
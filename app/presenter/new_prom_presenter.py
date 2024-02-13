from qfluentwidgets import FluentIcon
from ..view.home.dialog.new_prom_dialog import NewPromotionDialog
from ..models.model.prom_model import PromotionModel
from ..models.entity.promotion import Promotion

class NewPromotionPresenter:

    def __init__(self, view, model:PromotionModel, parentPresenter):
        self.view = view
        self.model = model
        self.parentPresenter = parentPresenter
        
    def dialogNew(self, event):
        dialog = NewPromotionDialog(self.view)
        if dialog.exec():
            name = dialog.nameLineEdit.text()
            rank = dialog.rankLineEdit.text()
            logo = dialog.logoLineEdit.text()
            years = dialog.yearLineEdit.text()
            prom = Promotion(name=name, rank=rank, logo=logo, years=years)
            self.model.create(prom)
            self.parentPresenter.fetchProm()
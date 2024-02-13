from qfluentwidgets import FluentIcon
from ..view.home.dialog.new_prom_dialog import NewPromotionDialog
from ..models.model.prom_model import PromotionModel
from ..models.entity.promotion import Promotion

class NewPromotionPresenter:

    def __init__(self, view, model:PromotionModel, parentPresenter):
        self.view = view
        self.model = model
        self.parentPresenter = parentPresenter
        
    def dialogNew(self, event, **kwargs):
        dialog = NewPromotionDialog(self.view)
        isUpdate = False
        promotion = None
        if len(kwargs) != 0:
            isUpdate = True
            promotion = kwargs.get("promotion")
            dialog.nameLineEdit.setText(promotion.name)
            dialog.rankLineEdit.setText(promotion.rank)
            dialog.logoLineEdit.setText(promotion.logo)
            dialog.yearLineEdit.setText(promotion.years)
            dialog.yesButton.setText("Mettre à jour")
        if dialog.exec():
            name = dialog.nameLineEdit.text()
            rank = dialog.rankLineEdit.text()
            logo = dialog.logoLineEdit.text()
            years = dialog.yearLineEdit.text()
            if isUpdate:
                self.model.update_item(promotion.id, name=name, rank=rank, logo=logo, years=years)
            else:
                prom = Promotion(name=name, rank=rank, logo=logo, years=years)
                self.model.create(prom)
            self.parentPresenter.fetchProm()
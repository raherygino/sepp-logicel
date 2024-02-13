from qfluentwidgets import FluentIcon
from .new_prom_presenter import NewPromotionPresenter
from ..models.model.prom_model import PromotionModel

class PromotionPresenter:

    def __init__(self, view, model: PromotionModel):
        self.view = view
        self.model = model
        self.nPromPresenter = NewPromotionPresenter(view, model, self)
        self.fetchProm()

    def fetchProm(self):
        layout = self.view.banner.linkCardView.hBoxLayout
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            widget.deleteLater()
            
        self.btnAdd = self.view.banner.btnAdd()
        self.btnAdd.mouseReleaseEvent = lambda event: self.nPromPresenter.dialogNew(event)
        
        promotions = self.model.fetch_all_items(order="id DESC")
        for promotion in promotions:
            self.view.banner.linkCardView.addCard(
                FluentIcon.PEOPLE,
                promotion.rank,
                promotion.name,
            )
        
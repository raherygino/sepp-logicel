from qfluentwidgets import FluentIcon, RoundMenu, Action, MenuAnimationType, Dialog
from .new_prom_presenter import NewPromotionPresenter
from ..models.model.prom_model import PromotionModel
from ..components.link_card2 import LinkCard
from PyQt5.QtCore import Qt

class PromotionPresenter:

    def __init__(self, view, model: PromotionModel):
        self.view = view
        self.model = model
        self.nPromPresenter = NewPromotionPresenter(view, model, self)
        self.fetchProm()
        
    def deleteBannerWidget(self):
        layout = self.view.banner.linkCardView.hBoxLayout
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            widget.deleteLater()
        
    def fetchProm(self):
        self.deleteBannerWidget()
        self.btnAdd = self.view.banner.btnAdd()
        self.btnAdd.mouseReleaseEvent = lambda event: self.nPromPresenter.dialogNew(event)
        
        promotions = self.model.fetch_all_items(order="id DESC")
        for promotion in promotions:
            card = LinkCard(
                FluentIcon.PEOPLE, 
                promotion.rank, 
                promotion.name, 
                self.view.banner.linkCardView)
            card.contextMenuEvent = lambda event, promotion=promotion: self.menuCard(event, promotion)            
            self.view.banner.linkCardView.hBoxLayout.addWidget(card, 0, Qt.AlignLeft)
            
    def menuCard(self, event, promotion):
        menu = RoundMenu(self.view)
        menu.addAction(Action(FluentIcon.FOLDER, 'Voir'))
        menu.addAction(
            Action(
                FluentIcon.EDIT, 
                'Modifier', 
                triggered=lambda event : self.nPromPresenter.dialogNew(event, promotion=promotion)
                )
            )
        menu.addSeparator()
        menu.addAction(
            Action(
                FluentIcon.DELETE, 
                'Supprimer', 
                triggered=lambda: self.deletePromotion(promotion)
                )
            )
        menu.exec(event.globalPos(), aniType=MenuAnimationType.DROP_DOWN)
        
    def deletePromotion(self, promotion):
        title = 'Vous êtes sûr de vouloir supprimer?'
        content = f'Quand vous avez supprimés {promotion.rank}, toutes les données avec cette promotion seront perdues'
        w = Dialog(title, content, self.view)
        w.setTitleBarVisible(False)
        if w.exec():
            self.model.delete_item(promotion.id)
            self.fetchProm()
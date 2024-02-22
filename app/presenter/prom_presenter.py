from qfluentwidgets import FluentIcon, RoundMenu, Action, MenuAnimationType, Dialog
from .new_prom_presenter import NewPromotionPresenter
from ..models.model.prom_model import PromotionModel, Promotion
from ..components.link_card2 import LinkCard
from ..common.functions import Function
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLayout, QWidget

class PromotionPresenter:

    def __init__(self, view, model: PromotionModel, mainWindow):
        self.view = view
        self.model = model
        self.mainView = mainWindow
        self.func = Function()
        self.nPromPresenter = NewPromotionPresenter(view, model, self)
        self.fetchProm()
        
    def deleteBannerWidget(self):
        layout = self.view.flowLayout
        #print(self.view.flowLayout._items)
        #layout.childern
        layout.takeAllWidgets()
        '''while layout.count():
            item = layout.takeAt(0)
            #widget = item.widget()
            item.deleteLater()'''
        
    def fetchProm(self):
        self.deleteBannerWidget()
        self.btnAdd = LinkCard(FluentIcon.ADD, 'Ajouter', 'Ajouter une autre promotion', self.view)
        self.btnAdd.mouseReleaseEvent = lambda event: self.nPromPresenter.dialogNew(event)
        
        promotions = self.model.fetch_all_items(order="id DESC")
        self.view.flowLayout.addWidget(self.btnAdd)
        for promotion in promotions:
            logo = FluentIcon.PEOPLE
            if promotion.logo != "":
                logo = promotion.logo
            card = LinkCard(
                logo, 
                promotion.rank, 
                promotion.name, 
                self.view)
            card.contextMenuEvent = lambda event, promotion=promotion: self.menuCard(event, promotion)
            card.mouseDoubleClickEvent = lambda event, promotion=promotion: self.showPromotion(event, promotion)            
            self.view.flowLayout.addWidget(card)
        #self.view.flowLayout.addWidget(self.btnAdd)
        #print(self.view.flowLayout.count())
        '''widgets = []
        for i in range(self.view.flowLayout.count()):
            item = self.view.flowLayout.itemAt(i)
            if isinstance(item, QLayout):
                widgets.extend(item.widget().findChildren(QWidget))
            else:
                widget = item.widget()
                if widget is not None:
                    #widgets.append(widget)
                    widget.deleteLayer()'''
            
    def showPromotion(self, event, promotion):
        studentInterface = self.mainView.studentInterface
        studentInterface.addTab(promotion)
        self.mainView.switchTo(studentInterface)
        
    def menuCard(self, event, promotion):
        menu = RoundMenu(self.view)
        menu.addAction(Action(FluentIcon.FOLDER, 'Voir', triggered=lambda event: self.showPromotion(event, promotion)))
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
            pos = None
            for i, item in enumerate(self.mainView.studentInterface.tabItems):
                if item == promotion.rank.replace(" ", "-"):
                    pos = i
            if pos != None:
                self.mainView.studentInterface.removeTab(pos)
            self.model.delete_item(promotion.id)
            if promotion.logo != "":
                self.func.deleteFile(promotion.logo)
            self.fetchProm()
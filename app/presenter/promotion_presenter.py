from qfluentwidgets import FluentIcon, RoundMenu, Action, MenuAnimationType, Dialog
from ..components.link_card2 import LinkCard
#from ..common.functions import Function
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLayout, QWidget
from ..models import PromotionModel, Promotion
from ..view.promotion import ListPromInterface, NewPromotionDialog

class PromotionPresenter:

    def __init__(self, view:ListPromInterface, model: PromotionModel):
        self.view = view
        self.model = model
        #self.func = Function()
        self.fetchProm()
        
    def deleteBannerWidget(self):
        layout = self.view.flowLayout
        layout.takeAllWidgets()
        
    def fetchProm(self):
        self.deleteBannerWidget()
        self.btnAdd = LinkCard(FluentIcon.ADD, 'Ajouter', 'Ajouter une autre promotion', self.view)
        self.btnAdd.mouseReleaseEvent = lambda event: self.showDialogNew(event)
        
        promotions = self.model.fetch_all(order="id DESC")
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
            #card.mouseDoubleClickEvent = lambda event, promotion=promotion: self.showPromotion(event, promotion)            
            self.view.flowLayout.addWidget(card)
            
    def showDialogNew(self, event):
        dialog = NewPromotionDialog(self.view)
        if dialog.exec():
            rank = dialog.rankcompactSpinBox.spinbox.text()
            name = dialog.nameLineEdit.lineEdit.text()
            year = dialog.yearLineEdit.lineEdit.text()
            promotion = Promotion(rank=rank, name=name, years=year, logo=dialog.logoPath)
            self.model.create(promotion)
            self.fetchProm()
            
    '''def showPromotion(self, event, promotion):
        studentInterface = self.mainView.studentInterface
        studentInterface.addTab(promotion)
        self.mainView.switchTo(studentInterface)'''
        
    def menuCard(self, event, promotion):
        menu = RoundMenu(self.view)
        menu.addAction(Action(FluentIcon.ACCEPT, 'Selectionner', triggered=lambda event: self.showPromotion(event, promotion)))
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
            self.model.delete(id=promotion.id)
            self.fetchProm()
        '''if w.exec():
            pos = None
            for i, item in enumerate(self.mainView.studentInterface.tabItems):
                if item == promotion.rank.replace(" ", "-"):
                    pos = i
            if pos != None:
                self.mainView.studentInterface.removeTab(pos)
            self.model.delete_item(promotion.id)
            if promotion.logo != "":
                self.func.deleteFile(promotion.logo)
            self.fetchProm()'''
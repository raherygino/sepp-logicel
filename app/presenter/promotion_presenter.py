from qfluentwidgets import FluentIcon, RoundMenu, Action, MenuAnimationType, Dialog
from ..components.link_card2 import LinkCard
from ..common.functions import Function
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLayout, QWidget
from ..models import PromotionModel, Promotion
from ..view.promotion import ListPromInterface, NewPromotionDialog

class PromotionPresenter:

    def __init__(self, view:ListPromInterface, model: PromotionModel):
        self.view = view
        self.mainView = self.view.parent
        self.model = model
        self.func = Function()
        self.fetchProm()
        
    def deleteBannerWidget(self):
        layout = self.view.flowLayout
        layout.takeAllWidgets()
        
    def fetchProm(self):
        self.deleteBannerWidget()
        self.btnAdd = LinkCard(FluentIcon.ADD, 'Ajouter', 'Ajouter une autre promotion', self.view)
        self.btnAdd.mouseReleaseEvent = lambda event: self.showDialogNew(event)
        promotions = self.model.fetch_all(order="id DESC")
        
        self.maxRank = self.model.max_col("rank")
        self.view.flowLayout.addWidget(self.btnAdd)
        for promotion in promotions:
            logo = FluentIcon.PEOPLE
            if promotion.logo != "":
                logo = promotion.logo
            card = LinkCard(
                logo, 
                str(promotion.rank), 
                promotion.name, 
                self.view)
            card.contextMenuEvent = lambda event, promotion=promotion: self.menuCard(event, promotion)
            card.mouseDoubleClickEvent = lambda event, promotion=promotion: self.showPromotion(event, promotion)            
            self.view.flowLayout.addWidget(card)
        self.mainView.checkPromotion(self.model)
            
    def showDialogNew(self, event, **kwargs):
        dialog = NewPromotionDialog(self.view)
        dialog.rankcompactSpinBox.spinbox.setValue(self.maxRank+1)
        
        if len(kwargs):
            promotion = kwargs.get("promotion")
            rank = dialog.rankcompactSpinBox.spinbox
            name = dialog.nameLineEdit.lineEdit
            year = dialog.yearLineEdit.lineEdit

            rank.setValue(promotion.rank)
            name.setText(promotion.name)
            year.setText(promotion.years)
            
            if len(promotion.logo) != 0:
                dialog.logoPath = promotion.logo
                dialog.logo.setPixmap(QPixmap(promotion.logo))
                dialog.logo.setFixedSize(180,180)
            
        if dialog.exec():
            rank = dialog.rankcompactSpinBox.spinbox.text()
            name = dialog.nameLineEdit.lineEdit.text()
            year = dialog.yearLineEdit.lineEdit.text()
            nwLogo = ""
            if (len(dialog.logoPath) != 0):
                if len(kwargs):
                    promotion = kwargs.get("promotion")
                    if dialog.logoPath != promotion.logo:
                        nwLogo = self.func.copyFileToFolderApp(dialog.logoPath, name=f"logo_{rank.replace(" ", "_")}")
                        self.func.deleteFile(promotion.logo)
                else:
                    nwLogo = self.func.copyFileToFolderApp(dialog.logoPath, name=f"logo_{rank.replace(" ", "_")}")
                    
            promotion = Promotion(rank=rank, name=name, years=year, logo=nwLogo)
            proms = self.model.fetch_by_condition(rank=rank)
            if len(kwargs):
                oldProm = kwargs.get("promotion")
                if len(proms) == 0:
                    self.model.update_item(oldProm.id, rank = rank, name=name, years=year, logo=nwLogo)
                    self.fetchProm()
                else:
                    if proms[0].rank == oldProm.rank:
                        self.model.update_item(oldProm.id, name=name, years=year, logo=nwLogo)
                        self.fetchProm()
                    else:
                        self.func.errorMessage("Erreur", "Rang existe déjà", self.mainView)
            else: 
                if len(proms) == 0:
                    self.model.create(promotion)
                    self.fetchProm()
                else:
                    self.func.errorMessage("Erreur", "Rang existe déjà", self.mainView)
    
    def showPromotion(self, event, promotion):
        dialog = NewPromotionDialog(self.view)
        
        rank = dialog.rankcompactSpinBox.spinbox
        name = dialog.nameLineEdit.lineEdit
        year = dialog.yearLineEdit.lineEdit
        
        rank.setReadOnly(True)
        rank.setDisabled(True)
        rank.setValue(promotion.rank)
        
        name.setReadOnly(True)
        name.setClearButtonEnabled(False)
        name.setText(promotion.name)
        
        year.setClearButtonEnabled(False)
        year.setReadOnly(True)
        year.setText(promotion.years)
        
        if len(promotion.logo) != 0:
            dialog.logo.setPixmap(QPixmap(promotion.logo))
            dialog.logo.setFixedSize(180,180)
        
        dialog.btnAddLogo.setVisible(False)
        dialog.yesButton.setVisible(False)
        dialog.exec()
        
    def menuCard(self, event, promotion):
        menu = RoundMenu(self.view)
        menu.addAction(Action(FluentIcon.FOLDER, 'Ouvrir', triggered=lambda event: self.showPromotion(event, promotion)))
        menu.addAction(Action(FluentIcon.EDIT, 'Modifier', triggered=lambda event : self.showDialogNew(event, promotion=promotion)))
        menu.addSeparator()
        menu.addAction(Action(FluentIcon.DELETE, 'Supprimer', triggered=lambda: self.deletePromotion(promotion)))
        menu.exec(event.globalPos(), aniType=MenuAnimationType.DROP_DOWN)
        
    def deletePromotion(self, promotion):
        title = 'Vous êtes sûr de vouloir supprimer?'
        content = f'Quand vous avez supprimés {promotion.rank}, toutes les données avec cette promotion seront perdues'
        w = Dialog(title, content, self.view)
        w.setTitleBarVisible(False)
        if w.exec():
            self.model.delete(id=promotion.id)
            if promotion.logo != "":
                self.func.deleteFile(promotion.logo)
            self.fetchProm()
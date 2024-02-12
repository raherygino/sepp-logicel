from qfluentwidgets import FluentIcon

class PromotionPresenter:

    def __init__(self, view, model):
        self.view = view
        self.model = model
        #self.fetchProm()
        self.btnAdd = self.view.banner.btnAdd()
        self.btnAdd.mouseReleaseEvent = lambda event: self.dialogNew(event)

    def dialogNew(self, event):
        self.view.showDialogNew()

    def fetchProm(self):
        self.view.banner.linkCardView.addCard(
            FluentIcon.ADD,
            'Ajouter',
            'Vous pouvez importer les élèves de la promotion',
        )
        print(self.view.banner.linkCardView.hBoxLayout.children())
        
from ..view.home.home_interface import HomeInterface
from ..models import PromotionModel, StudentModel


class HomePresenter:

    def __init__(self, view:HomeInterface, promModel: PromotionModel, studentModel: StudentModel):
        self.view = view
        #self.mainView = self.view.parent
        self.promModel = promModel
        self.studentModel = studentModel
        #self.func = Function()
        self.prom = 0
        self.view.current_prom.connect(lambda value: self.changePromotion(value))
        self.view.all_prom.connect(lambda prom: self.getAllPromotion(prom))
        self.view.choicePromotion.currentTextChanged.connect(lambda text: self.setProm(text))
        self.view.refresh.connect(self.isRefreshed)
        
    def isRefreshed(self):
        self.view.cardEffectif.content.setText(str(self.studentModel.count()))
        self.view.cardEffectifEip.content.setText(str(self.studentModel.count(grade="EIP")))
        self.view.cardEffectifEap.content.setText(str(self.studentModel.count(grade="EAP")))
        self.view.cardEffectifMan.content.setText(str(self.studentModel.count(genre="M")))
        self.view.cardEffectifWoman.content.setText(str(self.studentModel.count(genre="F")))
    
    def setProm(self, prom):
        self.view.current_prom.emit(int(prom))
        
    def changePromotion(self, value):
        self.currentPromotion = value
        self.view.currentProm = value
    
    def getAllPromotion(self, promotions):
        listProm = []
        for promotion in promotions:
            listProm.append(str(promotion.rank))
        self.view.choicePromotion.clear()
        self.view.choicePromotion.addItems(listProm)
        #print(self.prom)
        
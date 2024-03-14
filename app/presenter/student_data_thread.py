from qfluentwidgets import RoundMenu, Action, FluentIcon, MenuAnimationType, MessageBox, Dialog
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import QPoint, QThread, pyqtSignal, QTimer
from PyQt5.QtWidgets import QLineEdit, QFileDialog
from ..models import StudentModel, Student, MouvementModel, Mouvement, ComportementModel, Comportement
from ..common import Function
from ..components import TableView
from ..view.students.list_student_tab import ListStudent
from ..view.students.new_student_dialog import NewStudentDialog
from ..view.students.show_student_dialog import ShowStudentDialog
from ..view.students.new_movement_dialog import NewMouvementDialog
from ..view.home.dialog.new_comp_dialog import NewComportementDialog
import os
from docx import Document

class DataThread(QThread):
    update_progress = pyqtSignal(int)
    finished = pyqtSignal()

    def __init__(self, data, model:MouvementModel, parent=None):
        super(DataThread, self).__init__(parent)
        self.data = data
        self.model = model
        self.listStudent = []
        self.data2 = self.model.fetch_all_items()
    
    def findMove(self, col, value, move):
        isFound = move.find(f'{col}=\'{value}\'')
        if str(type(value)).find('str') != -1:
            if value.find('\'') != -1:
                isFound = move.find(f'{col}=\"{value}\"')
        return isFound != -1
    
    def countMove(self, idStudent, key, valType, mouvements):
        length = 0
        cod = []
        for move in mouvements:
            if self.findMove('idStudent', idStudent, move):
                if self.findMove(key, valType, move):
                    cod.append(eval(move))
        length = len(cod)
        return length
    
    def countTypeNsubTypeMove(self, idStudent, key, valType, valSub, mouvements):
        length = 0
        cod = []
        for move in mouvements:
            if self.findMove('idStudent', idStudent, move):
                if self.findMove(key, valType, move):
                    if self.findMove("subType", valSub, move):
                        cod.append(eval(move))
        length = len(cod)
        return length
    
    def sumMove(self, idStudent, key, valType, mouvements):
        length = 0
        cod = []
        for move in mouvements:
            if self.findMove('idStudent', idStudent, move):
                if self.findMove(key, valType, move):
                    mouvement = eval(move)
                    if mouvement.day != "":
                        length += int(mouvement.day)
        
        return length    

    def run(self):
        label_permission = NewMouvementDialog.typesMove[0]
        label_rm = NewMouvementDialog.typesMove[1]
        label_exant = NewMouvementDialog.subType[0][1]
        label_anm = NewMouvementDialog.typesMove[3]
        label_codis = NewMouvementDialog.subType[1][0]
        label_hors_tour = NewMouvementDialog.subType[1][1]
        label_bemolenge = NewMouvementDialog.subType[1][2]
        label_pert_eff_pol = NewMouvementDialog.subType[1][3]
        label_sanc_disc = NewMouvementDialog.typesMove[2]
        label_other = NewMouvementDialog.subType[1][4]
        label_lettre_fel = NewMouvementDialog.subType[2][0]
        label_remark_pos = NewMouvementDialog.typesMove[4]
        mouvements = []
        # Update progress bar and emit signals
        total = len(self.data2) + len(self.data)
        for i, row in enumerate(self.data2):
            # Simulate processing delay
            self.msleep(10)
            progress = int((i + 1) / total * 100)
            self.update_progress.emit(progress)
            mouvements.append(str(row))
            
        for i, student in enumerate(self.data):
            if i < 10:
                self.msleep(100)
            else:
                self.msleep(0)
            rm = self.sumMove(student.id, 'type', label_rm, mouvements)
            exant = self.sumMove(student.id, 'subType', label_exant, mouvements)
            permission = self.sumMove(student.id, 'type', label_permission, mouvements)
            codis = self.countMove(student.id, 'subType', label_codis, mouvements)
            bomelenge = self.countMove(student.id, 'subType', label_bemolenge, mouvements)
            hors_tour = self.sumMove(student.id, 'subType', label_hors_tour, mouvements)
            pert_eff_pol = self.countMove(student.id, 'subType', label_pert_eff_pol, mouvements)
            other_sanc = self.countTypeNsubTypeMove(student.id, "type", label_sanc_disc, label_other, mouvements)
            other_remark = self.countTypeNsubTypeMove(student.id, "type", label_remark_pos, label_other, mouvements)
            anm = self.sumMove(student.id, 'type', label_anm, mouvements)
            lettre_fel = self.countMove(student.id, 'subType', label_lettre_fel, mouvements)
            self.listStudent.append([
                student.matricule, student.level, student.lastname,
                student.firstname, student.gender, rm,exant,permission,
                codis,bomelenge, hors_tour, pert_eff_pol,
                other_sanc, anm, lettre_fel,other_remark])
                    
            progress = int((i + 1) / total * 100)
            self.update_progress.emit(progress)
        self.finished.emit()

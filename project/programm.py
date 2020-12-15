import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QErrorMessage
from project.mainwin import Ui_MainWindow
from project.salonwin import Ui_choose_salon
from project.myregwin import Ui_my_register


class RegisterForm(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.i = ''
        self.salons1 = Salons()
        self.registers = Registers()
        self.pushButton.clicked.connect(self.description_add)
        self.flag = False
        self.save_button.clicked.connect(self.button_function)
        self.check_register.clicked.connect(self.registers.show)
        self.data_salons = {}
        self.procedure_and_salon = {}
        self.data_procedures = {}
        self.load_db()
        self.load_main()

    def button_function(self):
        if self.name.text() and self.flag == True:
            self.salons1.show()
            self.flag = False
            with open("datapersons", "a") as file:
                file.write(self.name.text() + ',')
                file.write(str(self.procedures.currentText()) + ',')
        else:
            error_dialog = QErrorMessage()
            error_dialog.showMessage("Введены не все данные")
            error_dialog.exec_()

    def load_db(self):
        con = sqlite3.connect("MyDataBase.db")
        cur = con.cursor()
        names_procedures = []
        descriptions = []
        list_names_procedures = cur.execute("""SELECT name_procedure, salon FROM procedure""").fetchall()
        list_descriptions = cur.execute("""SELECT description FROM procedure""").fetchall()
        for elem in list_names_procedures:
            if elem[0] not in names_procedures:
                names_procedures.append(elem[0])
        for elem in list_descriptions:
            if elem[0] not in descriptions:
                descriptions.append(elem[0])
        for i in range(len(names_procedures)):
            self.data_procedures[names_procedures[i]] = descriptions[i]
        for i in range(len(list_names_procedures)):
            if list_names_procedures[i][0] not in self.procedure_and_salon.keys():
                self.procedure_and_salon[list_names_procedures[i][0]] = [list_names_procedures[i][1]]
            else:
                self.procedure_and_salon[list_names_procedures[i][0]].append(list_names_procedures[i][1])
        self.data_salons = cur.execute("""SELECT * FROM salon""").fetchall()
        con.close()

    def load_main(self):
        for i in self.data_procedures:
            self.procedures.addItem(i)

    def description_add(self):
        text = self.procedures.currentText()
        for i in self.data_procedures.keys():
            if i == text:
                self.description_procedure.clear()
                self.description_procedure.appendPlainText(self.data_procedures[i])
                self.description_procedure.setReadOnly(True)
        self.flag = True


class Salons(QWidget, Ui_choose_salon):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.data_salons = {}
        self.flag = False
        self.time = ''
        self.date = ''
        self.data_procedures = {}
        self.load_db()
        self.load_choose()
        self.pushButton.clicked.connect(self.description_add)
        self.save_register.clicked.connect(self.register)

    def load_choose(self):
        for i in self.data_salons:
            self.choose_sal.addItem(i[1])

    def load_db(self):
        con = sqlite3.connect("MyDataBase.db")
        cur = con.cursor()
        names_procedures = []
        descriptions = []
        list_names_procedures = cur.execute("""SELECT name_procedure, salon FROM procedure""").fetchall()
        list_descriptions = cur.execute("""SELECT description FROM procedure""").fetchall()
        for elem in list_names_procedures:
            if elem[0] not in names_procedures:
                names_procedures.append(elem[0])
        for elem in list_descriptions:
            if elem[0] not in descriptions:
                descriptions.append(elem[0])
        for i in range(len(names_procedures)):
            self.data_procedures[names_procedures[i]] = descriptions[i]
        '''for i in range(len(list_names_procedures)):
            if list_names_procedures[i][0] not in self.procedure_and_salon.keys():
                self.procedure_and_salon[list_names_procedures[i][0]] = [list_names_procedures[i][1]]
            else:
                self.procedure_and_salon[list_names_procedures[i][0]].append(list_names_procedures[i][1])'''
        self.data_salons = cur.execute("""SELECT * FROM salon""").fetchall()
        con.close()

    def description_add(self):
        self.flag = True
        text = self.choose_sal.currentText()
        for i in self.data_salons:
            if i[1] == text:
                self.description_salon.clear()
                st = f"{i[2]}\n{i[3]} "
                self.description_salon.appendPlainText(st)
                self.description_salon.setReadOnly(True)

    def register(self):
        if self.flag:
            self.flag = False
            self.date = self.dateTimeEdit.dateTime().toString('dd-MM-yyyy')
            self.time = self.dateTimeEdit.dateTime().toString('hh:mm')
            with open("datapersons", 'a') as file:
                file.write(self.choose_sal.currentText() + ',')
                file.write(self.date + ',')
                file.write(self.time)
                file.write('\n')
            self.close()
        else:
            error_dialog = QErrorMessage()
            error_dialog.showMessage("Введены не все данные")
            error_dialog.exec_()


class Registers(QWidget, Ui_my_register):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.okbutton.clicked.connect(self.button)

    def button(self):
        self.listWidget.clear()
        lst = []
        if self.name_r.text():
            with open("datapersons", "r") as file:
                for line in file:
                    lst.append(line.split(','))
        date = self.calendarWidget.selectedDate().toString("dd-MM-yyyy")
        name = self.name_r.text()
        for elem in lst:
            if elem[0] == name and elem[3] == date:
                self.listWidget.addItem(f"{elem[4]} {elem[1]} {elem[2]}")


sys._excepthook = sys.excepthook


def exception_hook(exctype, value, traceback):
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)


sys.excepthook = exception_hook


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = RegisterForm()
    ex.show()
    sys.exit(app.exec_())
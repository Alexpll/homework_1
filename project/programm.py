import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from project.mainwin import Ui_MainWindow
from project.salonwin import Ui_choose_salon
from project.myregwin import Ui_my_register


class RegisterForm(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.salons = Salons()
        self.registers = Registers()
        self.save_button.clicked.connect(self.salons.show)
        self.check_register.clicked.connect(self.registers.show)

    def check(self):
        pass


class Salons(QWidget, Ui_choose_salon):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


class Registers(QWidget, Ui_my_register):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


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
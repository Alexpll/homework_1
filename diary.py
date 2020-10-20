import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from ui_diary import Ui_MainWindow


class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.date = ''
        self.dict_tasks = {}
        self.setupUi(self)

        self.add_task.clicked.connect(self.addtask)
        self.calendarWidget.clicked['QDate'].connect(self.show_date_func)

    def show_date_func(self):
        self.list_tasks.clear()
        days = int(self.textEdit_2.toPlainText()) if self.textEdit_2.toPlainText() else 0
        date = self.calendarWidget.selectedDate().addDays(-1 * days)
        self.date = date.toString('dd-MM-yyyy')
        if self.date in self.dict_tasks.keys():
            for x in self.dict_tasks[self.date]:
                self.list_tasks.addItem(x)

    def addtask(self):
        textboxValue = self.textEdit_2.toPlainText()
        if textboxValue != '':
            self.textEdit_2.clear()
            if self.date in self.dict_tasks:
                self.dict_tasks[self.date].append(textboxValue)
            else:
                self.dict_tasks[self.date] = [textboxValue]
        else:
            pass


sys._excepthook = sys.excepthook


def exception_hook(exctype, value, traceback):
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)


sys.excepthook = exception_hook


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())

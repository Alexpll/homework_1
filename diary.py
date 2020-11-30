import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from ui_diary import Ui_MainWindow


class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.dict_tasks = {}
        self.check()
        self.date = ''
        self.setupUi(self)

        self.add_task.clicked.connect(self.addtask)
        self.calendarWidget.clicked['QDate'].connect(self.show_date_func)

    def check(self):
        with open("date.txt", 'r') as date:
            for line in date:
                x, y = line.split(' : ')
                y = y.strip('[')
                y = y.strip(']')
                y = y.strip("'")
                y = y.strip("']\n")
                a = y.split(', ')
                a = list(map(lambda x: x.strip("'"), a))
                self.dict_tasks[x] = a

    def show_date_func(self):
        self.list_tasks.clear()
        days = int(self.textEdit_2.toPlainText()) if self.textEdit_2.toPlainText() else 0
        date = self.calendarWidget.selectedDate().addDays(-1 * days)
        self.date = date.toString('dd-MM-yyyy')
        if self.date in self.dict_tasks.keys():
            for x in self.dict_tasks[self.date]:
                self.list_tasks.addItem(x)

    def sort_dict(self):
        for x, y in self.dict_tasks.items():
            lst = []
            for i in y:
                time, _ = i.split('  ')
                h, m = time.split(':')
                check = int(h + m)
                lst.append((check, i))
                lst = sorted(lst, key=lambda lst: lst[0])
            self.dict_tasks[x] = [x[1] for x in lst]

    def addtask(self):
        textboxValue = self.textEdit_2.toPlainText()
        if textboxValue != '':
            self.textEdit_2.clear()
            if self.date in self.dict_tasks:
                time_check = self.timeEdit.time()
                time_now = time_check.toString('hh:mm')
                self.dict_tasks[self.date].append(f'{time_now}  {textboxValue}')
            else:
                time_check = self.timeEdit.time()
                time_now = time_check.toString('hh:mm')
                self.dict_tasks[self.date] = [f'{time_now}  {textboxValue}']
            self.sort_dict()
            with open("date.txt", 'w') as date:
                lst = []
                for x, y in self.dict_tasks.items():
                    lst.append(f'{x} : {y}')
                date.write('\n'.join(lst))
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
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
import sys
import csv
from random import randint


from ikea.ui_table_form import Ui_MainWindow


class TableForm(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.load_table("ikea.csv")
        #self.save_table()
        self.color_row(3, 125)
        #self.pushButton.clicked.connect(self.save_table)

    def color_row(self, row, color):
        for i in range(self.tableWidget.columnCount()):
            self.tableWidget.item(row, i).setBackground(color)

    def load_table(self, file_name):
        with open(file_name, encoding="utf8") as csvfile:
            reader = csv.reader(csvfile, delimiter=';', quotechar='"')
            title = next(reader)
            self.tableWidget.setColumnCount(len(title))
            self.tableWidget.setHorizontalHeaderLabels(title)
            self.tableWidget.setRowCount(0)
            for i, row in enumerate(reader):
                self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
                for j, elem in enumerate(row):
                    self.tableWidget.setItem(i, j, QTableWidgetItem(elem))
        self.tableWidget.resizeColumnsToContents()


def excepthook(exctype, value, traceback):
    sys.__excepthook__(exctype, value, traceback)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    sys.excepthook = excepthook
    ex = TableForm()
    ex.show()
    sys.exit(app.exec())

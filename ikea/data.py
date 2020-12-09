import PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from PyQt5 import Qt
import sys
import csv
from random import randint


from ikea.ui_table_form import Ui_MainWindow


class TableForm(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.load_table("ikea.csv")
        self.save_table()
        self.pushButton.clicked.connect(self.save_table)
        self.color_row()

    def color_row(self):
        for i in range(5):
            color = QtGui.QColor(randint(0, 255), randint(0, 255), randint(0, 255))
            for j in range(self.tableWidget.columnCount()):
                self.tableWidget.item(i, j).setBackground(color)

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
                    if j == 1:
                        elem = ' ' * (5 - len(elem)) + elem
                    self.tableWidget.setItem(i, j, QTableWidgetItem(elem))
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.sortItems(1, order=QtCore.Qt.DescendingOrder)

    def save_table(self):
        file_name = self.lineEditFile.text()
        if file_name:
            with open(file_name, 'w', newline='') as csvfile:
                writer = csv.writer(
                    csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                writer.writerow([self.tableWidget.horizontalHeaderItem(i).text()
                                 for i in range(self.tableWidget.columnCount())])
                for i in range(self.tableWidget.rowCount()):
                    row = []
                    for j in range(self.tableWidget.columnCount()):
                        item = self.tableWidget.item(i, j)
                        if item is not None:
                            row.append(item.text())
                    writer.writerow(row)


def excepthook(exctype, value, traceback):
    sys.__excepthook__(exctype, value, traceback)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    sys.excepthook = excepthook
    ex = TableForm()
    ex.show()
    sys.exit(app.exec())

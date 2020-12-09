import PyQt5
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QComboBox
from PyQt5 import Qt
import sys
import csv
from olimpiada import Ui_MainWindow


class TableForm(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.load_table("rez.csv", '-', '-')
        self.check.clicked.connect(self.filters)
        self.box()

    def load_table(self, file_name, school, classes):
        with open("rez.csv", encoding="utf8") as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            title = next(reader)
            self.tableWidget.setColumnCount(len(title))
            self.tableWidget.setHorizontalHeaderLabels(title)
            self.tableWidget.setRowCount(0)
            # list_schools = []
            for i, row in enumerate(reader):
                self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
                if classes != '-' and school != '-':
                    if row[2][-7] + row[2][-6] == f"{school}" or row[2][-8] + row[2][-7] == f"{school}":
                        if row[2][-4] + row[2][-3] == f"{classes}" or row[2][-5] + row[2][-4] == f"{classes}":
                            for j, elem in enumerate(row):
                                self.tableWidget.setItem(i, j, QTableWidgetItem(elem))
                elif classes == '-' and school != '-':
                    if row[2][-7] + row[2][-6] == f"{school}" or row[2][-8] + row[2][-7] == f"{school}":
                        for j, elem in enumerate(row):
                            self.tableWidget.setItem(i, j, QTableWidgetItem(elem))
                elif school == '-' and classes != '-':
                    if row[2][-4] + row[2][-3] == f"{classes}" or row[2][-5] + row[2][-4] == f"{classes}":
                        for j, elem in enumerate(row):
                            self.tableWidget.setItem(i, j, QTableWidgetItem(elem))
                else:
                    for j, elem in enumerate(row):
                        self.tableWidget.setItem(i, j, QTableWidgetItem(elem))
            self.tableWidget.resizeColumnsToContents()
            self.tableWidget.sortItems(1, order=QtCore.Qt.DescendingOrder)

    def box(self):
        with open("classes") as file:
            for line in file:
                lst = line.split(' ')
            for elem in lst:
                self.number_class.addItem(elem)
        with open("schools") as file:
            for line in file:
                lst = line.split(' ')
            for elem in lst:
                self.number_school.addItem(elem)

    def filters(self):
        school = self.number_school.currentText()
        classes = self.number_class.currentText()
        self.load_table('rez.csv', school, classes)


def excepthook(exctype, value, traceback):
    sys.__excepthook__(exctype, value, traceback)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    sys.excepthook = excepthook
    ex = TableForm()
    ex.show()
    sys.exit(app.exec())

# pyuic5 olimpiada.ui -o olimpiada.py

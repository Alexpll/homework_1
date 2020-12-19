from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QDialog, QErrorMessage
import sys
import sqlite3


from crud.ui_table_form import Ui_MainWindow
from crud.ui_create_form import Ui_Dialog


class CreateForm(QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.mydb = "Mydbsalon.db"
        self.pushButtonOk.clicked.connect(self.ok_func)
        self.pushButton_2.clicked.connect(self.cancel_func)

    def ok_func(self):
        id_salon = self.lineEdit.text()
        name_salon = self.lineEdit_2.text()
        opening = self.lineEdit_3.text()
        address = self.lineEdit_4.text()
        database_connection = sqlite3.connect(self.mydb)
        cursor = database_connection.cursor()
        print(id_salon, id_salons)
        if str(id_salon) not in id_salons and id_salon and name_salon and opening and address and id_salon.isdigit():
            cursor.execute(f'''INSERT INTO salon VALUES (?, ?, ?, ?)''', (id_salon, name_salon, opening, address))
            database_connection.commit()
            database_connection.close()
            global per
            per = [id_salon, name_salon, opening, address]
            self.close()
        else:
            print('error')

    def cancel_func(self):
        global per
        per = []
        self.close()


class TableForm(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.mydb = "Mydbsalon.db"
        self.load_table()
        self.flag = False
        self.pushButtonDelete.clicked.connect(self.delete_row)
        self.tableWidget.itemChanged.connect(self.save_table)
        self.pushButtonCreate.clicked.connect(self.create_row)

    def load_table(self):
        title = ["id_salon", "name_salon", "opening", "address"]
        self.tableWidget.setColumnCount(len(title))
        self.tableWidget.setHorizontalHeaderLabels(title)
        self.tableWidget.setRowCount(0)
        database_connection = sqlite3.connect(self.mydb)
        cursor = database_connection.cursor()
        data_films = cursor.execute("SELECT * FROM salon").fetchall()
        for i, film in enumerate(data_films):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(film):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.sortItems(0, order=QtCore.Qt.AscendingOrder)
        database_connection.close()

    def save_table(self, item):
        if not self.flag:
            row = item.row()
            column = item.column()
            print(item.text())
            elem = [self.tableWidget.item(row, i).text() for i in range(4)]
            print(elem)
            database_connection = sqlite3.connect(self.mydb)
            cursor = database_connection.cursor()
            if column == 0:
                pass
                cursor.execute(f'''UPDATE salon 
                        SET id_salon = ?, name_salon = ?, opening = ?, address = ?
                        WHERE name_salon = ? AND opening = ?
                        ''', (elem[0], elem[1], elem[2], elem[3], elem[1], elem[2]))
            else:
                cursor.execute(f'''UPDATE salon 
                        SET id_salon = ?, name_salon = ?, opening = ?, address = ?
                        WHERE id_salon = ?
                        ''', (elem[0], elem[1], elem[2], elem[3], elem[0]))
            database_connection.commit()
            database_connection.close()
        else:
            self.flag = False

    def delete_row(self):
        database_connection = sqlite3.connect(self.mydb)
        cursor = database_connection.cursor()
        index = self.tableWidget.selectionModel().selectedRows()
        if len(index) == 1:
            elem_id = self.tableWidget.item(index[0].row(), 0).text()
            print(f'''DELETE FROM salon 
                                WHERE id_salon = {elem_id}
                                ''')
            cursor.execute(f'''DELETE FROM salon 
                                WHERE id_salon = {elem_id}
                                ''')
            self.tableWidget.removeRow(index[0].row())

        database_connection.commit()
        database_connection.close()

    def create_row(self):
        global id_salons
        id_salons = [self.tableWidget.item(i, 0).text() for i in range(self.tableWidget.rowCount())]
        form = CreateForm()
        form_result = form.exec()
        global per
        if per:
            rows = self.tableWidget.rowCount()
            self.flag = True
            self.tableWidget.setRowCount(rows + 1)
            self.tableWidget.setItem(rows, 0, QTableWidgetItem(str(per[0])))
            self.flag = True
            self.tableWidget.setItem(rows, 1, QTableWidgetItem(str(per[1])))
            self.flag = True
            self.tableWidget.setItem(rows, 2, QTableWidgetItem(str(per[2])))
            self.flag = True
            self.tableWidget.setItem(rows, 3, QTableWidgetItem(str(per[3])))
            self.tableWidget.sortItems(0, order=QtCore.Qt.AscendingOrder)


per = []
id_salons = []


def excepthook(exctype, value, traceback):
    sys.__excepthook__(exctype, value, traceback)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    sys.excepthook = excepthook
    ex = TableForm()
    ex.show()
    sys.exit(app.exec())
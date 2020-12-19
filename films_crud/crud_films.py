from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QDialog
import sys
import csv
from random import randint
import sqlite3


from films_crud.ui_table_form import Ui_MainWindow
from films_crud.ui_create_form import Ui_Dialog


class CreateForm(QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.films_db = "films.db"
        self.pushButtonOk.clicked.connect(self.ok_func)
        self.pushButton_2.clicked.connect(self.cancel_func)
        print(genres_lst)

    def ok_func(self):
        id_film = self.lineEdit.text()
        title = self.lineEdit_2.text()
        year = self.lineEdit_3.text()
        genre = self.lineEdit_4.text()
        duration = self.lineEdit_5.text()
        database_connection = sqlite3.connect(self.films_db)
        cursor = database_connection.cursor()
        lst_names_genres = [x[0] for x in genres_lst]
        if str(id_film) not in id_films and id_film and title and year and genre and genre in lst_names_genres \
                and (str(duration).isdigit() or duration == '') and str(year).isdigit():
            cursor.execute(f'''INSERT INTO films VALUES (?, ?, ?, ?, ?)''', (id_film, title, year, genre.index(genre) + 1, duration))
            database_connection.commit()
            database_connection.close()
            global per
            per = [id_film, title, year, genre, duration]
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
        self.films_db = "films.db"
        self.load_table()
        self.flag = False
        self.pushButtonDelete.clicked.connect(self.delete_row)
        self.tableWidget.itemChanged.connect(self.save_table)
        self.pushButtonCreate.clicked.connect(self.create_row)

    def color_row(self, row, color):
        for i in range(self.tableWidget.columnCount()):
            self.tableWidget.item(row, i).setBackground(color)

    def load_table(self):
        title = ["id", "title", "year", "genre", "duration"]
        self.tableWidget.setColumnCount(len(title))
        self.tableWidget.setHorizontalHeaderLabels(title)
        self.tableWidget.setRowCount(0)
        database_connection = sqlite3.connect(self.films_db)
        cursor = database_connection.cursor()
        data_films = cursor.execute("SELECT * FROM films").fetchall()
        for i, film in enumerate(data_films):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(film):
                global genres_lst
                if j == 0:
                    elem = ' ' * (5 - len(str(elem))) + str(elem)
                if j == 3:
                    if str(elem).isdigit():
                        ind = elem
                        elem = cursor.execute(f"SELECT title FROM genres "
                                              f"WHERE id = {elem}").fetchone()[0]
                        if (elem, ind) not in genres_lst:
                            genres_lst.append((elem, ind))
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.sortItems(0, order=QtCore.Qt.AscendingOrder)
        database_connection.close()

    def save_table(self, item):
        if not self.flag:
            row = item.row()
            column = item.column()
            print(item.text())
            elem = [self.tableWidget.item(row, i).text() for i in range(5)]
            database_connection = sqlite3.connect(self.films_db)
            cursor = database_connection.cursor()
            elem[3] = cursor.execute(f'SELECT id FROM genres WHERE title = "{elem[3]}"').fetchone()[0]
            if column == 0:
                pass
                cursor.execute(f'''UPDATE films 
                                    SET id = {elem[0]}, title = "{elem[1]}", year = {elem[2]}, genre = {elem[3]}, duration = {elem[4]}
                                    WHERE title = "{elem[1]}" AND year = {elem[2]} 
                                    ''')
            else:
                cursor.execute(f'''UPDATE films 
                        SET id = {elem[0]}, title = "{elem[1]}", year = {elem[2]}, genre = {elem[3]}, duration = {elem[4]}
                        WHERE id = {elem[0]}
                        ''')
            database_connection.commit()
            database_connection.close()
        else:
            self.flag = False

    def delete_row(self):
        database_connection = sqlite3.connect(self.films_db)
        cursor = database_connection.cursor()
        index = self.tableWidget.selectionModel().selectedRows()
        if len(index) == 1:
            elem_id = self.tableWidget.item(index[0].row(), 0).text()
            print(f'''DELETE FROM films 
                                WHERE id = {elem_id}
                                ''')
            cursor.execute(f'''DELETE FROM films 
                                WHERE id = {elem_id}
                                ''')
            self.tableWidget.removeRow(index[0].row())

        database_connection.commit()
        database_connection.close()

    def create_row(self):
        global id_films
        id_films = [self.tableWidget.item(i, 0).text() for i in range(self.tableWidget.rowCount())]
        form = CreateForm()
        form_result = form.exec()
        global per
        if per:
            rows = self.tableWidget.rowCount()
            self.flag = True
            self.tableWidget.setRowCount(rows + 1)
            self.tableWidget.setItem(rows, 0, QTableWidgetItem(' ' * (len(str(id_films[-1])) - len(str(per[0]))) + str(per[0])))
            self.flag = True
            self.tableWidget.setItem(rows, 1, QTableWidgetItem(str(per[1])))
            self.flag = True
            self.tableWidget.setItem(rows, 2, QTableWidgetItem(str(per[2])))
            self.flag = True
            self.tableWidget.setItem(rows, 3, QTableWidgetItem(str(per[3])))
            self.flag = True
            self.tableWidget.setItem(rows, 4, QTableWidgetItem(str(per[4])))
        self.tableWidget.sortItems(0, order=QtCore.Qt.AscendingOrder)


id_films = []
per = []
genres_lst = []


def excepthook(exctype, value, traceback):
    sys.__excepthook__(exctype, value, traceback)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    sys.excepthook = excepthook
    ex = TableForm()
    ex.show()
    sys.exit(app.exec())

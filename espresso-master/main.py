from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
import sqlite3
import sys

import PyQt5
from PyQt5 import uic
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import QApplication, QMessageBox, QPushButton, QInputDialog, QWidget, QVBoxLayout, QLabel, \
    QLineEdit, QComboBox
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)
        self.pushButton.clicked.connect(self.add)
        self.do()
        self.pushButton_3.clicked.connect(self.do)

    def add(self):
        self.dialog = Dialog()
        self.dialog.setWindowTitle("Форма")
        self.dialog.show()

    def do(self):
        self.con = sqlite3.connect("coffee.db")
        cur = self.con.cursor()
        result = cur.execute("SELECT * FROM coffee").fetchall()
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(len(result[0]))
        self.titles = [description[0] for description in cur.description]
        self.tableWidget.setHorizontalHeaderLabels(self.titles)
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))


class Dialog(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("addEditCoffeeForm.ui", self)
        self.pushButton5.clicked.connect(self.base)

    def base(self):
        nazvanie = self.lineEdit.text()
        prozharka = self.lineEdit_2.text()
        molotiy_vzernah = self.comboBox.currentText()
        vkus = self.lineEdit_3.text()
        cena = self.lineEdit_4.text()
        obyom = self.lineEdit_5.text()

        self.con = sqlite3.connect("coffee.db")
        cur = self.con.cursor()
        f = True
        result0 = cur.execute("SELECT * FROM coffee").fetchall()
        for i in result0:
            if nazvanie in i:
                f = False
        if f:
            cur.execute(
                "INSERT INTO coffee (name, stepen, molotyilivzernah, opisanie, cena, obyom) VALUES (?, ?, ?, ?, ?, ?)", (nazvanie, prozharka, molotiy_vzernah, vkus, cena, obyom))
            self.con.commit()
            cur.close()
        else:
            cur.execute(
                "UPDATE coffee set stepen = ?, molotyilivzernah = ?, opisanie = ?, cena = ?, obyom = ? WHERE name = ?",
                (prozharka, molotiy_vzernah, vkus, cena, obyom, nazvanie))
            self.con.commit()
            cur.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())

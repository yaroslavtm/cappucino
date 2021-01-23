import sqlite3
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QTableWidgetItem


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('UI_form.ui', self)
        self.loadTable()
        self.pushButton.clicked.connect(self.open_second_form)

    def loadTable(self):
        con = sqlite3.connect('coffee.sqlite')
        cur = con.cursor()
        reader = cur.execute('Select * from coffee').fetchall()
        self.len_ = len(reader)
        con.close()
        counter = 1
        for i, row in enumerate(reader):
            self.tableWidget.setRowCount(counter)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
            counter += 1
        self.tableWidget.resizeColumnsToContents()

    def open_second_form(self):
        self.second_form = secondForm()
        self.second_form.show()


class secondForm(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.initUI()

    def initUI(self):
        self.tableWidget.resizeColumnsToContents()
        self.comboBox.activated[str].connect(self.open_)
        self.combo_box()
        self.num = 'None'
        self.change.clicked.connect(self.change_element)
        self.add.clicked.connect(self.add_element)

    def combo_box(self):
        k = ['None']
        for i in range(ex.len_ + 1):
            k.append(str(i + 1))
        self.comboBox.addItems(k)

    def open_(self, text):
        self.num = text

    def change_element(self):
        if self.num != 'None' and ex.len_ > 0 and int(self.num) <= ex.len_:
            print('change')
            con = sqlite3.connect('coffee.sqlite')
            cur = con.cursor()
            albums = self.getData()
            titles = [description[0] for description in cur.description]
            for i in titles:
                cur.execute(f'UPDATE coffee SET {i} WHERE id=?', albums)
            con.commit()
            con.close()

    def add_element(self):
        if int(self.num) == ex.len_ + 1:
            con = sqlite3.connect('coffee.sqlite')
            cur = con.cursor()
            albums = self.getData()
            cur.execute('INSERT INTO coffee VALUES (?,?,?,?,?,?)', albums)
            con.commit()
            con.close()
            ex.loadTable()
            self.comboBox.addItems([str(int(self.num) + 1)])

    def getData(self):
        data = []
        cols = self.tableWidget.columnCount()
        for i in range(cols):
            item = self.tableWidget.item(0, i)
            if item != None:
                # print(item.text())
                data.append(item.text())
            else:
                data.append('')
        return data


app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(app.exec_())

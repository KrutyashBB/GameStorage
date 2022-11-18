import sqlite3
import sys

from PyQt5 import uic, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QHeaderView, QAction
from PyQt5.QtCore import Qt

from likes_win import LikesWindow
from sec_win import MyWidget2


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('library_design.ui', self)
        self.connection = sqlite3.connect("library_db.db")
        self.cur = self.connection.cursor()
        self.select_data()

    def select_data(self):
        self.setWindowTitle('Хранилище игр')
        self.setWindowIcon(QtGui.QIcon('icon.png'))

        self.likes = QAction(self)
        self.likes.setText('Избранное')
        self.likes.triggered.connect(self.about)
        self.menuBar().addAction(self.likes)
        self.menuBar().setStyleSheet('color: #FB8A2D; border: 1px solid #253261')

        self.searchEdit.textChanged.connect(self.search)
        self.tableWidget.cellClicked.connect(self.action_cell)

        title = [i[0] for i in
                 self.cur.execute("SELECT name FROM PRAGMA_TABLE_INFO('Games');").fetchall()]
        res = self.cur.execute("SELECT * FROM Games").fetchall()
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels(title)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.verticalHeader().hide()
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)

    def closeEvent(self, event):
        self.connection.close()

    def about(self):
        self.likes_window = LikesWindow()
        self.likes_window.show()

    def action_cell(self):
        row = self.tableWidget.currentRow()
        data = self.get_row_data(row)
        self.win2 = MyWidget2(data)
        self.win2.show()

    def get_row_data(self, row):
        data = []
        for i in range(self.tableWidget.columnCount()):
            data.append(self.tableWidget.item(row, i).text())
        return data

    def search(self, s):
        self.tableWidget.setCurrentItem(None)

        if not s or len(s) < 3:
            return

        matching_items = self.tableWidget.findItems(s, Qt.MatchContains)
        if matching_items:
            item = matching_items[0]
            self.tableWidget.setCurrentItem(item)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())

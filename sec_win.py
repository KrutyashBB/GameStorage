import sqlite3

from PyQt5 import uic, QtGui
from PyQt5.QtWidgets import QWidget, QMessageBox


class MyWidget2(QWidget):
    def __init__(self, data):
        super().__init__()
        uic.loadUi('sec_win_des.ui', self)

        self.data = data
        self.base = sqlite3.connect('library_db.db')
        self.cur = self.base.cursor()

        self.title, self.desc, self.platforms = self.data[1], self.data[2], self.data[3]
        self.developer, self.game_mode, self.release_date = self.data[4], self.data[5], self.data[6]

        self.unitUi()

    def unitUi(self):
        self.setWindowTitle('Описание игры')
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        self.description.setPlainText(self.desc)
        self.moreInformation.setPlainText(f'''Название: {self.title} \n
Платформы: {self.platforms} \n
Разработчик: {self.developer} \n
Режим игры: {self.game_mode} \n
Дата выхода: {self.release_date} \n''')

        self.addBtn.clicked.connect(self.add_likes)

    def add_likes(self):
        msg = QMessageBox()
        msg.setWindowTitle("Выполнено")
        msg.setIcon(QMessageBox.Information)
        msg.setWindowIcon(QtGui.QIcon('information_icon.png'))
        try:
            self.cur.execute('INSERT INTO LikesGames VALUES(?,?,?,?,?,?,?)', (self.data))
            self.base.commit()
            msg.setText("Игра успешна добавлена в избранное")
        except:
            msg.setText("Игра уже находится в избранном")
        msg.exec_()

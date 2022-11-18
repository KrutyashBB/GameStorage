import csv

import xlsxwriter
import sqlite3

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QHeaderView, QMessageBox, QFileDialog
from PyQt5 import QtGui, uic
from PyQt5 import QtCore


class LikesWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('likes_win_des.ui', self)

        self.base = sqlite3.connect("library_db.db")
        self.cur = self.base.cursor()

        self.searchEdit_2.textChanged.connect(self.search)
        self.clearBtn.clicked.connect(self.clear)
        self.unloadBtn.clicked.connect(self.unload)
        self.tableWidget_2.viewport().installEventFilter(self)

        self.unitUi()

    def unitUi(self):
        self.setWindowTitle('Избранное')
        self.setWindowIcon(QtGui.QIcon('icon.png'))

        self.title = [i[0] for i in
                      self.cur.execute("SELECT name FROM PRAGMA_TABLE_INFO('LikesGames');").fetchall()]
        res = self.cur.execute("SELECT * FROM LikesGames").fetchall()
        self.tableWidget_2.setColumnCount(7)
        self.tableWidget_2.setHorizontalHeaderLabels(self.title)
        self.tableWidget_2.setRowCount(0)
        for i, row in enumerate(res):
            self.tableWidget_2.setRowCount(
                self.tableWidget_2.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget_2.setItem(
                    i, j, QTableWidgetItem(str(elem)))

        self.tableWidget_2.verticalHeader().hide()
        self.tableWidget_2.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)

    def closeEvent(self, event):
        self.base.close()

    def search(self, s):
        self.tableWidget_2.setCurrentItem(None)

        if not s or len(s) < 3:
            return

        matching_items = self.tableWidget_2.findItems(s, Qt.MatchContains)
        if matching_items:
            item = matching_items[0]
            self.tableWidget_2.setCurrentItem(item)

    def eventFilter(self, source, event):
        if (event.type() == QtCore.QEvent.MouseButtonPress and event.buttons() == QtCore.Qt.LeftButton and
                source is self.tableWidget_2.viewport()):
            item = self.tableWidget_2.itemAt(event.pos())
            if item is not None:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Question)
                name = self.tableWidget_2.item(item.row(), 1).text()
                msg.setText(f"Вы действительно хотите удалить {name}?")
                msg.setWindowTitle("Подтверждение")
                msg.setWindowIcon(QtGui.QIcon('question-icon.png'))
                msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                retval = msg.exec_()
                if retval == QMessageBox.Ok:
                    row = item.row()
                    id = self.tableWidget_2.item(row, 0).text()
                    if self.tableWidget_2.rowCount() > 0:
                        self.tableWidget_2.removeRow(row)
                    self.cur.execute('DELETE FROM LikesGames WHERE id = ?', (id,))
                    self.base.commit()
        return super().eventFilter(source, event)

    def clear(self):
        if self.tableWidget_2.item(0, 0) is not None:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Question)
            msg.setText("Очистить всё?")
            msg.setWindowTitle("Подтверждение")
            msg.setWindowIcon(QtGui.QIcon('question-icon.png'))
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            retval = msg.exec_()
            if retval == QMessageBox.Ok:
                self.cur.execute('DELETE FROM LikesGames')
                self.base.commit()
                self.tableWidget_2.clearContents()
                self.tableWidget_2.setShowGrid(False)

        elif self.tableWidget_2.item(0, 0) is None:
            msg = QMessageBox()
            msg.setText("В таблице ничего нет")
            msg.setWindowTitle("Выполнено")
            msg.setIcon(QMessageBox.Information)
            msg.setWindowIcon(QtGui.QIcon('information_icon.png'))
            msg.exec_()

    def unload(self):
        msg = QMessageBox()

        def save_csv():
            file, check = QFileDialog.getSaveFileName(self, "Сохранить файл", "", "Text Files (*.csv)")
            if check:
                return file

        def save_xlsx():
            file, check = QFileDialog.getSaveFileName(self, "Сохранить файл", "", "Text Files (*.xlsx)")
            if check:
                return file

        def save_txt():
            file, check = QFileDialog.getSaveFileName(self, "Сохранить файл", "", "Text Files (*.txt)")
            if check:
                return file

        try:
            if self.changeBox.currentText() == 'EXCEL':
                msg.setText("EXCEL файл успешно создан")
                workbook = xlsxwriter.Workbook(save_xlsx())
                worksheet = workbook.add_worksheet()

                for i in range(len(self.title)):
                    worksheet.write(0, i, self.title[i])

                data = []
                for i in range(self.tableWidget_2.rowCount()):
                    row_data = []
                    for j in range(self.tableWidget_2.columnCount()):
                        item = self.tableWidget_2.item(i, j)
                        if item is not None:
                            row_data.append(item.text())
                    data.append(row_data)

                for row, item in enumerate(data):
                    for i in range(len(item)):
                        worksheet.write(row + 1, i, item[i])
                workbook.close()

            if self.changeBox.currentText() == 'CSV':
                msg.setText("CSV файл успешно создан")
                with open(save_csv(), 'w', newline='') as csvfile:
                    writer = csv.writer(
                        csvfile, delimiter=';', quotechar='"')
                    writer.writerow(self.title)
                    for i in range(self.tableWidget_2.rowCount()):
                        row = []
                        for j in range(self.tableWidget_2.columnCount()):
                            item = self.tableWidget_2.item(i, j)
                            if item is not None:
                                row.append(item.text())
                        writer.writerow(row)

            if self.changeBox.currentText() == 'TXT':
                msg.setText("TXT файл успешно создан")
                with open(save_txt(), 'w') as txtfile:
                    txtfile.write('\t'.join(self.title) + '\n')
                    for i in range(self.tableWidget_2.rowCount()):
                        row = []
                        for j in range(self.tableWidget_2.columnCount()):
                            item = self.tableWidget_2.item(i, j)
                            if item is not None:
                                row.append(item.text())
                        txtfile.write('\t'.join(row) + '\n')

            msg.setWindowTitle("Выполнено")
            msg.setIcon(QMessageBox.Information)
            msg.setWindowIcon(QtGui.QIcon('information_icon.png'))
            msg.exec_()
        except:
            pass

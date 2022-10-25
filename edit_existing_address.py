from typing import List
from PyQt5 import QtCore, QtGui, QtWidgets
from datetime import datetime
from distutils.log import error
import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
import sqlite3
from traceback import format_exc
import SanskritNames as sknames
import edit_sevadar_page


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class App(QWidget):
    def __init__(self):
        super().__init__()

        self.default_font = QtGui.QFont()
        self.default_font.setPointSize(13)
        self.setFont(self.default_font)

        self.title = 'Edit Existing Address'
        self.left = 0
        self.top = 0
        self.width = 1200
        self.height = 720

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.createTable()

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tableWidget)
        self.setLayout(self.layout)

        self.showMaximized()

    def createTable(self):
        self.tableWidget = QTableWidget()
        try:
            conn = sqlite3.connect('data\Seva_manager.db')
            conn.row_factory = dict_factory
            print("Opened database successfully")
            cur = conn.cursor()
            conn.commit()
            cur.execute(f"""
                select * from Addresses WHERE address_id != 0;
            """)
            addresses = cur.fetchall()
        except Exception as e:
            print(format_exc())
        finally:
            conn.close()

        # Row count
        self.tableWidget.setRowCount(len(addresses))
        # print(sevadars_details)

        # Column count
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(
            ['Address Id', 'Address', ''])

        for i, s in enumerate(addresses):
            self.tableWidget.setItem(
                i, 0, QTableWidgetItem(str(s['address_id'])))
            self.tableWidget.item(i, 0).setTextAlignment(
                QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)

            self.tableaddress = QLabel()
            self.tableaddress.setText(
                s['line1']+'\n'+s['line2']+'\n'+s['line3']+'\n'+s['line4'])
            self.tableaddress.setMargin(10)
            self.tableWidget.setCellWidget(i, 1, self.tableaddress)

            self.tableWidget.setItem(i, 2, QTableWidgetItem(type=2))
            edit_button = QPushButton()
            edit_button.setText('EDIT')
            edit_button.setFont(self.default_font)
            edit_button.setGeometry(QtCore.QRect(310, 390, 500, 50))
            edit_button.clicked.connect(
                lambda x, address=s: self.edit_address_callback(address))
            self.tableWidget.setCellWidget(i, 2, edit_button)

        self.tableWidget.verticalHeader().hide()
        self.tableWidget.horizontalHeader().setStyleSheet("""
            QHeaderView::section {padding: 10px; font-size: 13pt}
            """)
        self.tableWidget.setFont(self.default_font)
        self.default_font.setBold(True)
        self.tableWidget.horizontalHeader().setFont(self.default_font)

        self.tableWidget.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)
        self.tableWidget.verticalHeader().setSectionResizeMode(
            QHeaderView.ResizeToContents)

    def edit_address_callback(self, address):
        print('edit', address)
        d = QDialog()
        ui = Ui_Dialog(d)
        ui.setupUi(address)
        d.show()
        d.exec_()
        self.close()
        ex = App()


class Ui_Dialog(object):
    def __init__(self, d: QDialog) -> None:
        super().__init__()

        self.default_font = QtGui.QFont()
        self.default_font.setPointSize(12)
        self.dialog = d
        self.dialog.setFont(self.default_font)

        self.default_font = QtGui.QFont()
        self.default_font.setPointSize(15)

    def setupUi(self, address):
        self.address = address
        self.dialog.setMinimumSize(500, 275)

        self.verticalLayout_address_lines = QVBoxLayout(
            self.dialog)
        self.verticalLayout_address_lines.setObjectName(
            u"verticalLayout_address_lines")
        self.lineEdit_address: List[QLineEdit] = []
        for i in range(4):
            self.lineEdit_address.append(QLineEdit(address[f'line{i+1}']))
            self.lineEdit_address[i].setObjectName("lineEdit_address"+str(i))
            self.lineEdit_address[i].setEnabled(True)
            self.verticalLayout_address_lines.addWidget(
                self.lineEdit_address[i])
        self.verticalLayout_address_lines.setContentsMargins(40, 40, 40, 40)

        self.buttonBox = QtWidgets.QDialogButtonBox()
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(
            QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Save)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_address_lines.addWidget(self.buttonBox)

        self.buttonBox.accepted.connect(self.edit_save_callback)
        self.buttonBox.rejected.connect(self.dialog.reject)

    def edit_save_callback(self):
        print(self.address['line1'], self.lineEdit_address[0].text())

        try:
            conn = sqlite3.connect('data\Seva_manager.db')
            conn.row_factory = dict_factory
            print("Opened database successfully")
            cur = conn.cursor()
            cur.execute("PRAGMA foreign_keys=ON")
            conn.commit()
            set_statement = ''
            for i in range(4):
                set_statement += f'line{i+1} = "{self.lineEdit_address[i].text()}", '

            cur.execute(f"""
                UPDATE Addresses
                SET {set_statement[:-2]}
                WHERE address_id = {self.address['address_id']}
                """)
            conn.commit()
            print("Records created successfully")
        except Exception as e:
            print(format_exc())
        finally:
            conn.close()
        self.dialog.close()


if __name__ == '__main__':
    global app
    app = QApplication(sys.argv)
    global ex
    ex = App()
    sys.exit(app.exec())

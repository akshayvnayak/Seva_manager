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


class Ui_Dialog(object):
    def __init__(self, d) -> None:
        super().__init__()

        self.default_font = QtGui.QFont()
        self.default_font.setPointSize(12)

        self.d = d

    def setupUi(self, Dialog, s_id, s_name, ey, em):
        Dialog.setObjectName("Dialog")
        # Dialog.resize(482, 216)
        Dialog.setFont(self.default_font)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(70, 160, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(
            QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(40, 60, 383, 80))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout_2 = QtWidgets.QVBoxLayout(
            self.horizontalLayoutWidget)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(13)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.month_label = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.month_label.setObjectName("month_label")
        self.horizontalLayout.addWidget(self.month_label)
        self.month_comboBox = QtWidgets.QComboBox(self.horizontalLayoutWidget)
        self.month_comboBox.setEditable(False)
        self.month_comboBox.setMaxVisibleItems(12)
        self.month_comboBox.setIconSize(QtCore.QSize(20, 20))
        self.month_comboBox.setObjectName("month_comboBox")
        self.horizontalLayout.addWidget(self.month_comboBox)
        self.year_label = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.year_label.setObjectName("year_label")
        self.horizontalLayout.addWidget(self.year_label)
        self.year_spinBox = QtWidgets.QSpinBox(self.horizontalLayoutWidget)
        self.year_spinBox.setMinimum(2000)
        self.year_spinBox.setMaximum(9999)
        self.year_spinBox.setProperty("value", ey)
        self.year_spinBox.setDisplayIntegerBase(10)
        self.year_spinBox.setObjectName("year_spinBox")
        self.horizontalLayout.addWidget(self.year_spinBox)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        self.sevadar_name_label = QtWidgets.QLabel(Dialog)
        self.sevadar_name_label.setGeometry(QtCore.QRect(20, 10, 400, 31))
        self.sevadar_name_label.setObjectName("sevadar_name_label")
        self.default_font.setBold(True)
        self.sevadar_name_label.setFont(self.default_font)
        self.sevadar_name_label.setAlignment(QtCore.Qt.AlignCenter)

        self.error_msg = QtWidgets.QLabel(Dialog)
        self.error_msg.setGeometry(QtCore.QRect(40, 90, 400, 31))
        self.error_msg.setObjectName("error_msg")
        self.error_msg.setVisible(False)
        self.error_msg.setAutoFillBackground(True)

        self.retranslateUi(Dialog, s_id, s_name, ey, em)
        self.buttonBox.accepted.connect(lambda: self.renew_accept_callback(
            s_id, self.year_spinBox.text(), self.month_comboBox.currentIndex()+1, ey, em))  # type: ignore
        self.buttonBox.rejected.connect(Dialog.reject)  # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog, s_id, s_name, ey, em):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "New Pooja start date:"))
        self.month_label.setText(_translate("Dialog", "Month"))
        self.year_label.setText(_translate("Dialog", "Year"))
        self.sevadar_name_label.setText(
            _translate("Dialog", "Sevadar : " + s_name))
        self.error_msg.setText(_translate(
            "Dialog", "Renewal date cannot be less than previous ending date"))
        self.month_comboBox.addItems(sknames.months.values())
        self.month_comboBox.setCurrentIndex(em-1)
# Main Window

    def renew_accept_callback(self, sevadar_id, year, month, ey, em):
        e_date = datetime(ey, em, 1)
        entered_date = datetime(int(year), int(month), 1)
        if (entered_date < e_date):
            self.error_msg.setVisible(True)
            return

        try:
            conn = sqlite3.connect('data\Seva_manager.db')
            conn.row_factory = dict_factory
            print("Opened database successfully")
            cur = conn.cursor()
            cur.execute("PRAGMA foreign_keys=ON")
            conn.commit()
            cur.execute(f"""
                INSERT INTO SevaStartMonths values ({sevadar_id},'{year}-{format(month,'02d')}');
                """)
            conn.commit()
            print("Records created successfully")
        except Exception as e:
            print(format_exc())
        finally:
            conn.close()
        self.d.close()


class App(QWidget):
    def __init__(self, year, month):
        super().__init__()

        self.default_font = QtGui.QFont()
        self.default_font.setPointSize(13)
        self.setFont(self.default_font)

        self.year = year
        self.month = month
        self.title = 'Ending poojas from ' + \
            str(self.year)+'-'+format(self.month, '02')
        self.left = 0
        self.top = 0
        self.width = 1200
        self.height = 720

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.createTable(year, month)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tableWidget)
        self.setLayout(self.layout)

        self.showMaximized()

    def createTable(self, year, month):
        self.tableWidget = QTableWidget()

        # if month == 1:
        #     month = 12
        #     year -= 1
        # else:
        #     month = month - 1

        try:
            conn = sqlite3.connect('data\Seva_manager.db')
            conn.row_factory = dict_factory
            print("Opened database successfully")
            cur = conn.cursor()
            cur.execute("PRAGMA foreign_keys=ON")
            conn.commit()
            cur.execute(f"""
                select sevadar_id,name,start_yyyymm from sevadardetailsRecent 
                where start_yyyymm > "{year-1}-{format(month,'02d')}"
                order by start_yyyymm;
            """)
            sevadars_details = cur.fetchall()
        except Exception as e:
            print(format_exc())
        finally:
            conn.close()

        # Row count
        self.tableWidget.setRowCount(len(sevadars_details))
        # print(sevadars_details)

        # Column count
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setHorizontalHeaderLabels(
            ['Id', 'Name', 'Start month', 'End month', ''])

        for i, s in enumerate(sevadars_details):
            self.tableWidget.setItem(
                i, 0, QTableWidgetItem(str(s['sevadar_id'])))
            self.tableWidget.setItem(i, 1, QTableWidgetItem(s['name']))
            self.tableWidget.setItem(i, 2, QTableWidgetItem(s['start_yyyymm']))
            sy = int(s['start_yyyymm'][:4])
            sm = int(s['start_yyyymm'][5:7])
            if sm == 1:
                em = 12
                ey = sy
            else:
                em = sm - 1
                ey = sy+1

            self.tableWidget.setItem(
                i, 3, QTableWidgetItem(f"{ey}-{format(em,'02d')}"))

            self.tableWidget.setItem(i, 4, QTableWidgetItem(type=2))
            edit_button = QPushButton()
            edit_button.setText('RENEW')
            edit_button.setFont(self.default_font)
            edit_button.setGeometry(QtCore.QRect(310, 390, 500, 50))
            edit_button.clicked.connect(lambda x, sevadar_id=s['sevadar_id'], sevadar_name=s['name'], ey=ey, em=em: self.renew_callback(
                sevadar_id, sevadar_name, ey, em))
            self.tableWidget.setCellWidget(i, 4, edit_button)

            self.tableWidget.setRowHeight(i, 50)

        # self.tableWidget.resizeRowsToContents()
        # self.tableWidget.resizeColumnsToContents()

        self.tableWidget.verticalHeader().hide()
        # Table will fit the screen horizontally
        # self.tableWidget.horizontalHeader().setStretchLastSection(True)
        # self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # self.tableWidget.setStyleSheet("""
        #     QTableWidget::item {padding: 5px; font-size: 200px}
        #     """)

        self.tableWidget.horizontalHeader().setStyleSheet("""
            QHeaderView::section {padding: 10px; font-size: 13pt}
            """)
        self.tableWidget.setFont(self.default_font)
        self.default_font.setBold(True)
        self.tableWidget.horizontalHeader().setFont(self.default_font)

        self.tableWidget.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeToContents)

    def renew_callback(self, sevadar_id, sevadar_name, ey, em):
        print(sevadar_id, sevadar_name, 'renew')
        d = QDialog()
        ui = Ui_Dialog(d)
        if em == 12:
            em = 1
            ey += 1
        else:
            em += 1
        ui.setupUi(d, sevadar_id, sevadar_name, ey, em)
        d.show()
        d.exec_()
        self.close()
        ex = App(self.year, self.month)


if __name__ == '__main__':
    global app
    app = QApplication(sys.argv)
    global ex
    ex = App(2023, 1)
    sys.exit(app.exec())

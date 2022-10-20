# -*- coding: utf-8 -*-

from datetime import datetime
import sqlite3
from collections import namedtuple

import PyQt5
import SanskritNames
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets

import traceback


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def add_sevadar(sevadar_details_dict,window):
    window.close()
    sevadar_details = namedtuple("SevadarDetails", sevadar_details_dict.keys())(
        *sevadar_details_dict.values())
    print(sevadar_details)
    try:
        conn = sqlite3.connect('data\Seva_manager.db')
        # conn.row_factory = dict_factory
        print("Opened database successfully")
        cur = conn.cursor()
        cur.execute("PRAGMA foreign_keys=ON")
        conn.commit()
        cur.execute(f"""
            INSERT INTO Sevadars(name,rashi,nakshatra,gotra,pooja_basis,pooja_date)
            VALUES("{sevadar_details.name}",{sevadar_details.rashi},{sevadar_details.nakshatra},{sevadar_details.gotra},{sevadar_details.date_basis},{sevadar_details.date[sevadar_details.date_basis]});
        """)
        conn.commit()
        cur.execute('SELECT last_insert_rowid()')
        sevadar_id = cur.fetchone()[0]
        print(sevadar_id)
        if sevadar_details.flexible_flag:
            cur.execute(f"INSERT INTO SevadarsFlexible VALUES ({sevadar_id})")
        cur.execute(f"""
            INSERT INTO SevaStartMonths
            VALUES({sevadar_id},'{sevadar_details.start_month}');
        """)

        address_id = sevadar_details.address_id
        if sevadar_details.new_address_flag:
            cur.execute(f"""
                INSERT INTO Addresses (line1,line2,line3,line4)
                VALUES('{sevadar_details.address[0]}','{sevadar_details.address[1]}','{sevadar_details.address[2]}','{sevadar_details.address[3]}');
            """)
            conn.commit()
            cur.execute('SELECT last_insert_rowid()')
            address_id = cur.fetchone()[0]

        if sevadar_details.group_flag:
            conn.commit()
            cur.execute(
                f'SELECT * FROM GroupDetails WHERE address_id = {address_id}')
            existing_group = cur.fetchone()
            if existing_group == None:
                cur.execute(f'''
                    INSERT INTO GroupDetails(address_id)
                    VALUES({address_id});
                ''')
                conn.commit()
                cur.execute(f'SELECT last_insert_rowid();')
                group_id = cur.fetchone()[0]
            else:
                group_id = existing_group[0]
            cur.execute(f'''
                INSERT INTO Groups
                VALUES({sevadar_id},{group_id})
            ''')
        else:
            cur.execute(f"""
                INSERT INTO SevadarAddress
                VALUES({sevadar_id},{address_id});
            """)

        conn.commit()
        # cur.execute(f"""SELECT * FROM Sevadars
        # NATURAL JOIN SevaStartMonths
        # NATURAL JOIN PoojaDates
        # NATURAL JOIN SevadarAddress
        # NATURAL JOIN Addresses;""")
        # for row in cur.fetchall():
        #     print(row)
        # print(cur.fetchall())
    except Exception as e:
        print("Database error:", e)
        print(traceback.format_exc())
    finally:
        conn.close()
    window.close()


class Ui_MainWindow(QWidget):
    def __init__(self, window):
        super().__init__()

        
        self.default_font = QFont()
        self.default_font.setPointSize(15)

        self.setupUi(window)

    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1080, 720)
        MainWindow.setTabShape(QTabWidget.Rounded)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setFont(self.default_font)
        self.buttonBox = QDialogButtonBox(self.centralwidget)
        self.buttonBox.setObjectName(u"buttonBox")
        self.gridLayoutWidget = QWidget(self.centralwidget)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(200,20, 500, 400))
        
        self.buttonBox.setGeometry(QRect(450, 590, 300, 40))
        self.buttonBox.setStandardButtons(
            QDialogButtonBox.Cancel | QDialogButtonBox.Ok)

        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setSizeConstraint(QLayout.SetMinimumSize)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.label_date = QLabel(self.gridLayoutWidget)
        self.label_date.setObjectName(u"label_date")
        self.gridLayout.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_date, 7, 0, 1, 1)

        self.horizontalLayout_seva_start = QHBoxLayout()
        self.horizontalLayout_seva_start.setObjectName(
            u"horizontalLayout_seva_start")
        self.label_start_month = QLabel(self.gridLayoutWidget)
        self.label_start_month.setObjectName(u"label_start_month")
        self.label_start_month.setAlignment(
            Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)

        self.horizontalLayout_seva_start.addWidget(self.label_start_month)

        self.comboBox_start_month = QComboBox(self.gridLayoutWidget)
        self.comboBox_start_month.setObjectName(u"comboBox_start_month")

        self.horizontalLayout_seva_start.addWidget(self.comboBox_start_month)

        self.label_star_year = QLabel(self.gridLayoutWidget)
        self.label_star_year.setObjectName(u"label_star_year")
        self.label_star_year.setLayoutDirection(Qt.LeftToRight)
        self.label_star_year.setAlignment(
            Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)

        self.horizontalLayout_seva_start.addWidget(self.label_star_year)

        self.spinBox_start_year = QSpinBox(self.gridLayoutWidget)
        self.spinBox_start_year.setObjectName(u"spinBox_start_year")
        self.spinBox_start_year.setCursor(QCursor(Qt.ArrowCursor))
        self.spinBox_start_year.setMinimum(2000)
        self.spinBox_start_year.setMaximum(9999)

        
        self.current_date = datetime.now()
        self.spinBox_start_year.setValue(self.current_date.year if self.current_date.month!=1 else self.current_date.year+1)

        self.horizontalLayout_seva_start.addWidget(self.spinBox_start_year)

        self.horizontalLayout_seva_start.setStretch(1, 1)
        self.horizontalLayout_seva_start.setStretch(3, 1)

        self.gridLayout.addLayout(self.horizontalLayout_seva_start, 5, 2, 1, 1)

        self.label_nakshatra = QLabel(self.gridLayoutWidget)
        self.label_nakshatra.setObjectName(u"label_nakshatra")

        self.gridLayout.addWidget(self.label_nakshatra, 3, 0, 1, 1)

        self.horizontalLayout__date_basis = QHBoxLayout()
        self.horizontalLayout__date_basis.setObjectName(
            u"horizontalLayout__date_basis")
        self.horizontalLayout__date_basis.setSizeConstraint(
            QLayout.SetDefaultConstraint)

        self.radioButton_date_basis = []
        self.radioButtonGroup_date_basis = QtWidgets.QButtonGroup(MainWindow)
        for i in range(4):
            self.radioButton_date_basis.append(
                QRadioButton(self.gridLayoutWidget))
            self.radioButton_date_basis[i].setObjectName(
                "radioButton_date_basis_"+str(i))

            self.horizontalLayout__date_basis.addWidget(
                self.radioButton_date_basis[i])

            self.radioButtonGroup_date_basis.addButton(
                self.radioButton_date_basis[i], i)

        self.radioButton_date_basis[0].setChecked(True)

        self.checkBox_flexible = QCheckBox(self.gridLayoutWidget)
        self.checkBox_flexible.setObjectName(u"checkBox_flexible")

        self.horizontalLayout__date_basis.addWidget(self.checkBox_flexible)

        # self.radioButton_date = QRadioButton(self.gridLayoutWidget)
        # self.radioButton_date.setObjectName(u"radioButton_date")

        # self.horizontalLayout__date_basis.addWidget(self.radioButton_date)

        # self.radioButton_nakshatra = QRadioButton(self.gridLayoutWidget)
        # self.radioButton_nakshatra.setObjectName(u"radioButton_nakshatra")

        # self.horizontalLayout__date_basis.addWidget(self.radioButton_nakshatra)

        # self.radioButton_week = QRadioButton(self.gridLayoutWidget)
        # self.radioButton_week.setObjectName(u"radioButton_week")

        # self.horizontalLayout__date_basis.addWidget(self.radioButton_week)

        # self.radioButton_tithi = QRadioButton(self.gridLayoutWidget)
        # self.radioButton_tithi.setObjectName(u"radioButton_tithi")

        # self.horizontalLayout__date_basis.addWidget(self.radioButton_tithi)

        # self.radioButton_flexible = QRadioButton(self.gridLayoutWidget)
        # self.radioButton_flexible.setObjectName(u"radioButton_flexible")

        # self.horizontalLayout__date_basis.addWidget(self.radioButton_flexible)

        self.gridLayout.addLayout(
            self.horizontalLayout__date_basis, 6, 2, 1, 1)

        self.label_name = QLabel(self.gridLayoutWidget)
        self.label_name.setObjectName(u"label_name")

        self.gridLayout.addWidget(self.label_name, 0, 0, 1, 1)

        self.label_group = QLabel(self.gridLayoutWidget)
        self.label_group.setObjectName(u"label_group")

        self.gridLayout.addWidget(self.label_group, 9, 0, 1, 1)

        self.label_existing_address = QLabel(self.gridLayoutWidget)
        self.label_existing_address.setObjectName(u"label_existing_address")

        self.gridLayout.addWidget(self.label_existing_address, 8, 0, 1, 1)

        self.label_basis = QLabel(self.gridLayoutWidget)
        self.label_basis.setObjectName(u"label_basis")

        self.gridLayout.addWidget(self.label_basis, 6, 0, 1, 1)

        self.comboBox_gotra = QComboBox(self.gridLayoutWidget)
        self.comboBox_gotra.setObjectName(u"comboBox_gotra")

        self.gridLayout.addWidget(self.comboBox_gotra, 4, 2, 1, 1)

        self.label_address = QLabel(self.gridLayoutWidget)
        self.label_address.setObjectName(u"label_address")

        self.gridLayout.addWidget(self.label_address, 10, 0, 1, 1)

        self.lineEdit_name = QLineEdit(self.gridLayoutWidget)
        self.lineEdit_name.setObjectName(u"lineEdit_name")

        self.gridLayout.addWidget(self.lineEdit_name, 0, 2, 1, 1)

        self.verticalLayout_address = QVBoxLayout()
        self.verticalLayout_address.setObjectName(u"verticalLayout_address")
        self.comboBox_address = QComboBox(self.gridLayoutWidget)
        self.comboBox_address.setObjectName(u"comboBox_address")
        self.comboBox_address.setStyleSheet("QComboBox { combobox-popup: ; }");

        self.verticalLayout_address.addWidget(self.comboBox_address)

        self.verticalLayout_address_lines = QVBoxLayout()
        self.verticalLayout_address_lines.setObjectName(
            u"verticalLayout_address_lines")

        self.lineEdit_address = []
        for i in range(4):

            self.lineEdit_address.append(QLineEdit(self.gridLayoutWidget))
            self.lineEdit_address[i].setObjectName("lineEdit_address"+str(i))
            self.lineEdit_address[i].setEnabled(True)

            self.verticalLayout_address_lines.addWidget(
                self.lineEdit_address[i])

        # self.lineEdit_address1 = QLineEdit(self.gridLayoutWidget)
        # self.lineEdit_address1.setObjectName(u"lineEdit_address1")
        # self.lineEdit_address1.setEnabled(True)

        # self.verticalLayout_address_lines.addWidget(self.lineEdit_address1)

        # self.lineEdit_address2 = QLineEdit(self.gridLayoutWidget)
        # self.lineEdit_address2.setObjectName(u"lineEdit_address2")
        # self.lineEdit_address2.setEnabled(True)

        # self.verticalLayout_address_lines.addWidget(self.lineEdit_address2)

        # self.lineEdit_address3 = QLineEdit(self.gridLayoutWidget)
        # self.lineEdit_address3.setObjectName(u"lineEdit_address3")
        # self.lineEdit_address3.setEnabled(True)

        # self.verticalLayout_address_lines.addWidget(self.lineEdit_address3)

        # self.lineEdit_address4 = QLineEdit(self.gridLayoutWidget)
        # self.lineEdit_address4.setObjectName(u"lineEdit_address4")
        # self.lineEdit_address4.setEnabled(True)

        # self.verticalLayout_address_lines.addWidget(self.lineEdit_address4)

        self.verticalLayout_address.addLayout(
            self.verticalLayout_address_lines)

        self.gridLayout.addLayout(self.verticalLayout_address, 10, 2, 1, 1)

        self.horizontalLayout_group_yes_no = QHBoxLayout()
        self.horizontalLayout_group_yes_no.setObjectName(
            u"horizontalLayout_group_yes_no")

        self.radioButtonGroup_new_address = QtWidgets.QButtonGroup(MainWindow)

        self.radioButton_group_yes = QRadioButton(self.gridLayoutWidget)
        self.radioButton_group_yes.setObjectName(u"radioButton_group_yes")
        self.radioButton_group_yes.setContextMenuPolicy(Qt.DefaultContextMenu)
        self.radioButton_group_yes.setChecked(True)

        self.radioButtonGroup_new_address.addButton(self.radioButton_group_yes)
        self.horizontalLayout_group_yes_no.addWidget(
            self.radioButton_group_yes)

        self.radioButton_group_no = QRadioButton(self.gridLayoutWidget)
        self.radioButton_group_no.setObjectName(u"radioButton_group_no")

        self.radioButtonGroup_new_address.addButton(self.radioButton_group_no)
        self.horizontalLayout_group_yes_no.addWidget(self.radioButton_group_no)

        self.gridLayout.addLayout(
            self.horizontalLayout_group_yes_no, 9, 2, 1, 1)

        self.horizontalLayout_new_address = QHBoxLayout()
        self.horizontalLayout_new_address.setObjectName(
            u"horizontalLayout_new_address")

        self.radioButtonGroup_new_address = QtWidgets.QButtonGroup(MainWindow)

        self.radioButton_new_address = QRadioButton(self.gridLayoutWidget)
        self.radioButton_new_address.setObjectName(u"radioButton_new_address")
        self.radioButton_new_address.setContextMenuPolicy(
            Qt.DefaultContextMenu)
        self.radioButton_new_address.setChecked(True)

        self.radioButtonGroup_new_address.addButton(
            self.radioButton_new_address)
        self.horizontalLayout_new_address.addWidget(
            self.radioButton_new_address)

        self.radioButton_existing_address = QRadioButton(self.gridLayoutWidget)
        self.radioButton_existing_address.setObjectName(
            u"radioButton_existing_address")

        self.radioButtonGroup_new_address.addButton(
            self.radioButton_existing_address)
        self.horizontalLayout_new_address.addWidget(
            self.radioButton_existing_address)

        self.gridLayout.addLayout(
            self.horizontalLayout_new_address, 8, 2, 1, 1)

        self.label_seva_start = QLabel(self.gridLayoutWidget)
        self.label_seva_start.setObjectName(u"label_seva_start")

        self.gridLayout.addWidget(self.label_seva_start, 5, 0, 1, 1)

        self.verticalLayout_date_preference = QVBoxLayout()
        self.verticalLayout_date_preference.setSpacing(0)
        self.verticalLayout_date_preference.setObjectName(
            u"verticalLayout_date_preference")
        self.verticalLayout_date_preference.setSizeConstraint(
            QLayout.SetMinimumSize)
        self.verticalLayout_date_preference.setContentsMargins(0, -1, -1, -1)

        # self.verticalLayout_date_preference = QVBoxLayout()
        # self.verticalLayout_date_preference.setObjectName(u"verticalLayout_date_preference")
        self.spinBox_date = QSpinBox(self.gridLayoutWidget)
        self.spinBox_date.setObjectName(u"spinBox_date")
        self.spinBox_date.setMinimum(1)
        self.spinBox_date.setMaximum(31)

        self.verticalLayout_date_preference.addWidget(self.spinBox_date)

        self.comboBox_nakshatra_2 = QComboBox(self.gridLayoutWidget)
        self.comboBox_nakshatra_2.setObjectName(u"comboBox_nakshatra_2")

        self.verticalLayout_date_preference.addWidget(
            self.comboBox_nakshatra_2)

        self.horizontalLayout_day_week_no = QHBoxLayout()
        self.horizontalLayout_day_week_no.setObjectName(
            u"horizontalLayout_day_week_no")
        self.label_day = QLabel(self.gridLayoutWidget)
        self.label_day.setObjectName(u"label_day")
        self.label_day.setAlignment(
            Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)

        self.horizontalLayout_day_week_no.addWidget(self.label_day)

        self.comboBox_day = QComboBox(self.gridLayoutWidget)
        self.comboBox_day.setObjectName(u"comboBox_day")

        self.horizontalLayout_day_week_no.addWidget(self.comboBox_day)

        self.label_week = QLabel(self.gridLayoutWidget)
        self.label_week.setObjectName(u"label_week")
        self.label_week.setLayoutDirection(Qt.LeftToRight)
        self.label_week.setAlignment(
            Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)

        self.horizontalLayout_day_week_no.addWidget(self.label_week)

        self.spinBox_week_no = QSpinBox(self.gridLayoutWidget)
        self.spinBox_week_no.setObjectName(u"spinBox_week_no")
        self.spinBox_week_no.setCursor(QCursor(Qt.ArrowCursor))
        self.spinBox_week_no.setMinimum(1)
        self.spinBox_week_no.setMaximum(6)
        self.spinBox_week_no.setValue(1)

        self.horizontalLayout_day_week_no.addWidget(self.spinBox_week_no)

        self.horizontalLayout_day_week_no.setStretch(1, 1)
        self.horizontalLayout_day_week_no.setStretch(3, 1)

        self.verticalLayout_date_preference.addLayout(
            self.horizontalLayout_day_week_no)

        self.comboBox_tithi = QComboBox(self.gridLayoutWidget)
        self.comboBox_tithi.setObjectName(u"comboBox_tithi")

        self.verticalLayout_date_preference.addWidget(self.comboBox_tithi)

        self.gridLayout.addLayout(
            self.verticalLayout_date_preference, 7, 2, 1, 1)

        self.comboBox_nakshatra = QComboBox(self.gridLayoutWidget)
        self.comboBox_nakshatra.setObjectName(u"comboBox_nakshatra")

        self.gridLayout.addWidget(self.comboBox_nakshatra, 3, 2, 1, 1)

        self.label_rashi = QLabel(self.gridLayoutWidget)
        self.label_rashi.setObjectName(u"label_rashi")

        self.gridLayout.addWidget(self.label_rashi, 2, 0, 1, 1)

        self.comboBox_rashi = QComboBox(self.gridLayoutWidget)
        self.comboBox_rashi.setObjectName(u"comboBox_rashi")

        self.gridLayout.addWidget(self.comboBox_rashi, 2, 2, 1, 1)

        self.label_gotra = QLabel(self.gridLayoutWidget)
        self.label_gotra.setObjectName(u"label_gotra")

        self.gridLayout.addWidget(self.label_gotra, 4, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1079, 26))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi
        self.MainWindow = MainWindow
        self.connectUi()
        self.add_options()

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate(
            "MainWindow", u"Add Sevadar", None))
        self.label_date.setText(QCoreApplication.translate(
            "MainWindow", u"Seva date preference", None))
        self.label_start_month.setText(
            QCoreApplication.translate("MainWindow", u"Month", None))
        self.label_star_year.setText(
            QCoreApplication.translate("MainWindow", u"Year", None))
        self.label_nakshatra.setText(
            QCoreApplication.translate("MainWindow", u"Nakshatra", None))
        self.radioButton_date_basis[0].setText(
            QCoreApplication.translate("MainWindow", u"Date", None))
        self.radioButton_date_basis[1].setText(
            QCoreApplication.translate("MainWindow", u"Nakshatra", None))
        self.radioButton_date_basis[2].setText(
            QCoreApplication.translate("MainWindow", u"Week number and day", None))
        self.radioButton_date_basis[3].setText(
            QCoreApplication.translate("MainWindow", u"Tithi", None))
        self.checkBox_flexible.setText(
            QCoreApplication.translate("MainWindow", u"Flexible", None))
        self.label_name.setText(
            QCoreApplication.translate("MainWindow", u"Name", None))
        self.label_group.setText(QCoreApplication.translate(
            "MainWindow", u"Does this sevadar belong to a group?", None))

        self.label_existing_address.setText(QCoreApplication.translate(
            "MainWindow", u"New address or Existing address?", None))

        self.label_basis.setText(QCoreApplication.translate(
            "MainWindow", u"Seva date basis", None))
        self.label_address.setText(
            QCoreApplication.translate("MainWindow", u"Address", None))
        self.radioButton_group_yes.setText(
            QCoreApplication.translate("MainWindow", u"Yes", None))
        self.radioButton_group_no.setText(
            QCoreApplication.translate("MainWindow", u"No", None))

        self.radioButton_new_address.setText(
            QCoreApplication.translate("MainWindow", u"New address", None))
        self.radioButton_existing_address.setText(
            QCoreApplication.translate("MainWindow", u"Existing address", None))

        self.label_seva_start.setText(
            QCoreApplication.translate("MainWindow", u"Seva start", None))
        self.label_day.setText(
            QCoreApplication.translate("MainWindow", u"Day", None))
        self.label_week.setText(QCoreApplication.translate(
            "MainWindow", u"Week number", None))
        self.label_rashi.setText(
            QCoreApplication.translate("MainWindow", u"Rashi", None))
        self.label_gotra.setText(
            QCoreApplication.translate("MainWindow", u"Gotra", None))
    # retranslateUi
        self.gridLayout.setAlignment(Qt.AlignCenter)

    def connectUi(self):
        for i in self.radioButtonGroup_date_basis.buttons():
            i.clicked.connect(lambda: self.date_basis_radio_callback(
                self.radioButtonGroup_date_basis.checkedId()))
        self.date_basis_radio_callback(
            self.radioButtonGroup_date_basis.checkedId())

        # self.radioButton_group_yes.clicked.connect(lambda: self.group_yes_or_no_callback(False))
        # self.radioButton_group_no.clicked.connect(lambda: self.group_yes_or_no_callback(True))
        # self.group_yes_or_no_callback(False)

        self.radioButton_new_address.clicked.connect(
            lambda: self.new_address_callback(True))
        self.radioButton_existing_address.clicked.connect(
            lambda: self.new_address_callback(False))
        self.new_address_callback(True)

        self.buttonBox.accepted.connect(lambda: add_sevadar({
            "name": self.lineEdit_name.text(),
            "rashi": self.comboBox_rashi.currentIndex()+1,
            "nakshatra": self.comboBox_nakshatra.currentIndex()+1,
            "gotra": self.comboBox_gotra.currentIndex()+1,
            "start_month": self.spinBox_start_year.text()+"-"+format(self.comboBox_start_month.currentIndex()+1, "02d"),
            "date_basis": self.radioButtonGroup_date_basis.checkedId(),
            "date": (self.spinBox_date.value(),
                     self.comboBox_nakshatra_2.currentIndex()+1,
                     self.spinBox_week_no.value()*10+self.comboBox_day.currentIndex(),
                     self.comboBox_tithi.currentIndex()+1),
            "flexible_flag": self.checkBox_flexible.isChecked(),
            "new_address_flag": self.radioButton_new_address.isChecked(),
            "group_flag": self.radioButton_group_yes.isChecked(),
            "address_id": int(self.comboBox_address.currentText().split(',')[0]) if self.comboBox_address.currentText() != "" else -1,
            "address": [i.text() for i in self.lineEdit_address]
        },self.MainWindow))

        self.buttonBox.rejected.connect(lambda: self.MainWindow.close())

    def date_basis_radio_callback(self, index):
        setHidden_values = [True]*4
        setHidden_values[index] = False

        self.spinBox_date.setHidden(setHidden_values[0])

        self.comboBox_nakshatra_2.setHidden(setHidden_values[1])

        self.label_day.setHidden(setHidden_values[2])
        self.comboBox_day.setHidden(setHidden_values[2])
        self.label_week.setHidden(setHidden_values[2])
        self.spinBox_week_no.setHidden(setHidden_values[2])

        self.comboBox_tithi.setHidden(setHidden_values[3])

    def new_address_callback(self, state):
        self.comboBox_address.setHidden(state)

        for i in self.lineEdit_address:
            i.setHidden(not state)

    def add_options(self):
        self.comboBox_rashi.addItems(SanskritNames.rashis.values())
        self.comboBox_nakshatra.addItems(SanskritNames.nakshatras.values())
        self.comboBox_gotra.addItems(SanskritNames.gotras.values())
        self.comboBox_tithi.addItems(SanskritNames.tithis.values())
        self.comboBox_start_month.addItems(SanskritNames.months.values())
        self.comboBox_start_month.setCurrentIndex(self.current_date.month%12)
        self.comboBox_day.addItems(SanskritNames.vaaras.values())
        self.comboBox_nakshatra_2.addItems(SanskritNames.nakshatras.values())

        try:
            conn = sqlite3.connect('data\Seva_manager.db')
            cur = conn.cursor()
            cur.execute("PRAGMA foreign_keys=ON")
            conn.commit()
            addresses = cur.execute('SELECT * FROM Addresses').fetchall()
        except Exception as e:
            print(e)
        finally:
            conn.close()
        # print(addresses)
        for address in addresses:
            self.comboBox_address.addItem(str(address)[1:-1])


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    # x = QtWidgets.QAbstractScrollArea()
    ui = Ui_MainWindow(MainWindow)
    # ui.setupUi()
    MainWindow.showMaximized()
    sys.exit(app.exec_())

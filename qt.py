# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'testQmIXYH.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(999, 735)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.buttonBox = QDialogButtonBox(self.centralwidget)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(390, 590, 193, 28))
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.gridLayoutWidget = QWidget(self.centralwidget)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(80, 90, 814, 485))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.label_2 = QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        self.comboBox_3 = QComboBox(self.gridLayoutWidget)
        self.comboBox_3.setObjectName(u"comboBox_3")

        self.gridLayout.addWidget(self.comboBox_3, 3, 2, 1, 1)

        self.label_11 = QLabel(self.gridLayoutWidget)
        self.label_11.setObjectName(u"label_11")

        self.gridLayout.addWidget(self.label_11, 8, 0, 1, 1)

        self.label_7 = QLabel(self.gridLayoutWidget)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout.addWidget(self.label_7, 5, 0, 1, 1)

        self.label = QLabel(self.gridLayoutWidget)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.label_8 = QLabel(self.gridLayoutWidget)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout.addWidget(self.label_8, 4, 0, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.radioButton = QRadioButton(self.gridLayoutWidget)
        self.radioButton.setObjectName(u"radioButton")

        self.horizontalLayout_2.addWidget(self.radioButton)

        self.radioButton_3 = QRadioButton(self.gridLayoutWidget)
        self.radioButton_3.setObjectName(u"radioButton_3")

        self.horizontalLayout_2.addWidget(self.radioButton_3)

        self.radioButton_4 = QRadioButton(self.gridLayoutWidget)
        self.radioButton_4.setObjectName(u"radioButton_4")

        self.horizontalLayout_2.addWidget(self.radioButton_4)

        self.radioButton_2 = QRadioButton(self.gridLayoutWidget)
        self.radioButton_2.setObjectName(u"radioButton_2")

        self.horizontalLayout_2.addWidget(self.radioButton_2)

        self.radioButton_5 = QRadioButton(self.gridLayoutWidget)
        self.radioButton_5.setObjectName(u"radioButton_5")

        self.horizontalLayout_2.addWidget(self.radioButton_5)


        self.gridLayout.addLayout(self.horizontalLayout_2, 5, 2, 1, 1)

        self.label_3 = QLabel(self.gridLayoutWidget)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)

        self.label_4 = QLabel(self.gridLayoutWidget)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)

        self.lineEdit = QLineEdit(self.gridLayoutWidget)
        self.lineEdit.setObjectName(u"lineEdit")

        self.gridLayout.addWidget(self.lineEdit, 0, 2, 1, 1)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.spinBox = QSpinBox(self.gridLayoutWidget)
        self.spinBox.setObjectName(u"spinBox")

        self.verticalLayout.addWidget(self.spinBox)

        self.comboBox_5 = QComboBox(self.gridLayoutWidget)
        self.comboBox_5.setObjectName(u"comboBox_5")

        self.verticalLayout.addWidget(self.comboBox_5)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_12 = QLabel(self.gridLayoutWidget)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_4.addWidget(self.label_12)

        self.comboBox_7 = QComboBox(self.gridLayoutWidget)
        self.comboBox_7.setObjectName(u"comboBox_7")

        self.horizontalLayout_4.addWidget(self.comboBox_7)

        self.label_13 = QLabel(self.gridLayoutWidget)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setLayoutDirection(Qt.LeftToRight)
        self.label_13.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_4.addWidget(self.label_13)

        self.spinBox_4 = QSpinBox(self.gridLayoutWidget)
        self.spinBox_4.setObjectName(u"spinBox_4")
        self.spinBox_4.setCursor(QCursor(Qt.ArrowCursor))
        self.spinBox_4.setMinimum(1)
        self.spinBox_4.setMaximum(6)
        self.spinBox_4.setValue(1)

        self.horizontalLayout_4.addWidget(self.spinBox_4)

        self.horizontalLayout_4.setStretch(1, 1)
        self.horizontalLayout_4.setStretch(3, 1)

        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.comboBox_6 = QComboBox(self.gridLayoutWidget)
        self.comboBox_6.setObjectName(u"comboBox_6")

        self.verticalLayout.addWidget(self.comboBox_6)


        self.gridLayout.addLayout(self.verticalLayout, 6, 2, 1, 1)

        self.comboBox = QComboBox(self.gridLayoutWidget)
        self.comboBox.setObjectName(u"comboBox")

        self.gridLayout.addWidget(self.comboBox, 1, 2, 1, 1)

        self.label_9 = QLabel(self.gridLayoutWidget)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout.addWidget(self.label_9, 6, 0, 1, 1)

        self.comboBox_2 = QComboBox(self.gridLayoutWidget)
        self.comboBox_2.setObjectName(u"comboBox_2")

        self.gridLayout.addWidget(self.comboBox_2, 2, 2, 1, 1)

        self.label_10 = QLabel(self.gridLayoutWidget)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout.addWidget(self.label_10, 7, 0, 1, 1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.radioButton_6 = QRadioButton(self.gridLayoutWidget)
        self.radioButton_6.setObjectName(u"radioButton_6")

        self.horizontalLayout_3.addWidget(self.radioButton_6)

        self.radioButton_7 = QRadioButton(self.gridLayoutWidget)
        self.radioButton_7.setObjectName(u"radioButton_7")

        self.horizontalLayout_3.addWidget(self.radioButton_7)


        self.gridLayout.addLayout(self.horizontalLayout_3, 7, 2, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_5 = QLabel(self.gridLayoutWidget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout.addWidget(self.label_5)

        self.comboBox_4 = QComboBox(self.gridLayoutWidget)
        self.comboBox_4.setObjectName(u"comboBox_4")

        self.horizontalLayout.addWidget(self.comboBox_4)

        self.label_6 = QLabel(self.gridLayoutWidget)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setLayoutDirection(Qt.LeftToRight)
        self.label_6.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout.addWidget(self.label_6)

        self.spinBox_2 = QSpinBox(self.gridLayoutWidget)
        self.spinBox_2.setObjectName(u"spinBox_2")
        self.spinBox_2.setCursor(QCursor(Qt.ArrowCursor))
        self.spinBox_2.setMinimum(2000)
        self.spinBox_2.setMaximum(9999)
        self.spinBox_2.setValue(2021)

        self.horizontalLayout.addWidget(self.spinBox_2)

        self.horizontalLayout.setStretch(1, 1)
        self.horizontalLayout.setStretch(3, 1)

        self.gridLayout.addLayout(self.horizontalLayout, 4, 2, 1, 1)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.comboBox_8 = QComboBox(self.gridLayoutWidget)
        self.comboBox_8.setObjectName(u"comboBox_8")

        self.verticalLayout_2.addWidget(self.comboBox_8)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.lineEdit_2 = QLineEdit(self.gridLayoutWidget)
        self.lineEdit_2.setObjectName(u"lineEdit_2")

        self.verticalLayout_3.addWidget(self.lineEdit_2)

        self.lineEdit_5 = QLineEdit(self.gridLayoutWidget)
        self.lineEdit_5.setObjectName(u"lineEdit_5")

        self.verticalLayout_3.addWidget(self.lineEdit_5)

        self.lineEdit_4 = QLineEdit(self.gridLayoutWidget)
        self.lineEdit_4.setObjectName(u"lineEdit_4")

        self.verticalLayout_3.addWidget(self.lineEdit_4)

        self.lineEdit_3 = QLineEdit(self.gridLayoutWidget)
        self.lineEdit_3.setObjectName(u"lineEdit_3")

        self.verticalLayout_3.addWidget(self.lineEdit_3)


        self.verticalLayout_2.addLayout(self.verticalLayout_3)


        self.gridLayout.addLayout(self.verticalLayout_2, 8, 2, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 999, 26))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Rashi", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"Address", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Seva date basis", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Name", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Seva start", None))
        self.radioButton.setText(QCoreApplication.translate("MainWindow", u"Date", None))
        self.radioButton_3.setText(QCoreApplication.translate("MainWindow", u"Nakshatra", None))
        self.radioButton_4.setText(QCoreApplication.translate("MainWindow", u"Week number and day", None))
        self.radioButton_2.setText(QCoreApplication.translate("MainWindow", u"Tithi", None))
        self.radioButton_5.setText(QCoreApplication.translate("MainWindow", u"Flexible", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Nakshatra", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Gotra", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"Day", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"Week number", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Seva date preference", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"Does this sevadar belong to a group?", None))
        self.radioButton_6.setText(QCoreApplication.translate("MainWindow", u"Yes", None))
        self.radioButton_7.setText(QCoreApplication.translate("MainWindow", u"No", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Month", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Year", None))
    # retranslateUi


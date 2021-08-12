# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1079, 736)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.seva_date_basis = QtWidgets.QButtonGroup(MainWindow)
        self.seva_group_yesorno = QtWidgets.QButtonGroup(MainWindow)

        self.buttonBox = QtWidgets.QDialogButtonBox(self.centralwidget)
        self.buttonBox.setGeometry(QtCore.QRect(390, 610, 193, 28))
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(80, 80, 814, 514))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label_date = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_date.setObjectName("label_date")
        self.gridLayout.addWidget(self.label_date, 7, 0, 1, 1)
        self.horizontalLayout_seva_start = QtWidgets.QHBoxLayout()
        self.horizontalLayout_seva_start.setObjectName("horizontalLayout_seva_start")
        self.label_start_month = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_start_month.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_start_month.setObjectName("label_start_month")
        self.horizontalLayout_seva_start.addWidget(self.label_start_month)
        self.comboBox_start_month = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.comboBox_start_month.setObjectName("comboBox_start_month")
        self.horizontalLayout_seva_start.addWidget(self.comboBox_start_month)
        self.label_star_year = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_star_year.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_star_year.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_star_year.setObjectName("label_star_year")
        self.horizontalLayout_seva_start.addWidget(self.label_star_year)
        self.spinBox_start_year = QtWidgets.QSpinBox(self.gridLayoutWidget)
        self.spinBox_start_year.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.spinBox_start_year.setMinimum(2000)
        self.spinBox_start_year.setMaximum(9999)
        self.spinBox_start_year.setProperty("value", 2021)
        self.spinBox_start_year.setObjectName("spinBox_start_year")
        self.horizontalLayout_seva_start.addWidget(self.spinBox_start_year)
        self.horizontalLayout_seva_start.setStretch(1, 1)
        self.horizontalLayout_seva_start.setStretch(3, 1)

        self.gridLayout.addLayout(self.horizontalLayout_seva_start, 5, 2, 1, 1)
        self.label_nakshatra = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_nakshatra.setObjectName("label_nakshatra")
        self.gridLayout.addWidget(self.label_nakshatra, 3, 0, 1, 1)
        self.label_name = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_name.setObjectName("label_name")
        self.gridLayout.addWidget(self.label_name, 0, 0, 1, 1)
        self.label_group = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_group.setObjectName("label_group")
        self.gridLayout.addWidget(self.label_group, 8, 0, 1, 1)
        self.label_basis = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_basis.setObjectName("label_basis")
        self.gridLayout.addWidget(self.label_basis, 6, 0, 1, 1)
        self.comboBox_gotra = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.comboBox_gotra.setObjectName("comboBox_gotra")
        self.gridLayout.addWidget(self.comboBox_gotra, 4, 2, 1, 1)
        self.label_address = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_address.setObjectName("label_address")
        self.gridLayout.addWidget(self.label_address, 9, 0, 1, 1)
        self.lineEdit_name = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.lineEdit_name.setObjectName("lineEdit_name")
        self.gridLayout.addWidget(self.lineEdit_name, 0, 2, 1, 1)


        ############



        ###Yess or no option Group
        
        self.horizontalLayout_group_yes_no = QtWidgets.QHBoxLayout()
        self.horizontalLayout_group_yes_no.setObjectName("horizontalLayout_group_yes_no")
        self.radioButton_group_yes = QtWidgets.QRadioButton(self.gridLayoutWidget)
        self.radioButton_group_yes.setObjectName("radioButton_group_yes")
        self.horizontalLayout_group_yes_no.addWidget(self.radioButton_group_yes)
        self.radioButton_group_no = QtWidgets.QRadioButton(self.gridLayoutWidget)
        self.radioButton_group_no.setObjectName("radioButton_group_no")
        self.horizontalLayout_group_yes_no.addWidget(self.radioButton_group_no)
        

        self.gridLayout.addLayout(self.horizontalLayout_group_yes_no, 8, 2, 1, 1)



        self.horizontalLayout_seva_date_basis = QtWidgets.QHBoxLayout()
        self.horizontalLayout_seva_date_basis.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_seva_date_basis.setObjectName("horizontalLayout_seva_date_basis")
        self.radioButton_date = QtWidgets.QRadioButton(self.gridLayoutWidget)
        self.radioButton_date.setObjectName("radioButton_date")
        self.horizontalLayout_seva_date_basis.addWidget(self.radioButton_date)
        self.radioButton_nakshatra = QtWidgets.QRadioButton(self.gridLayoutWidget)
        self.radioButton_nakshatra.setObjectName("radioButton_nakshatra")
        self.horizontalLayout_seva_date_basis.addWidget(self.radioButton_nakshatra)
        self.radioButton_week = QtWidgets.QRadioButton(self.gridLayoutWidget)
        self.radioButton_week.setObjectName("radioButton_week")
        self.horizontalLayout_seva_date_basis.addWidget(self.radioButton_week)
        self.radioButton_tithi = QtWidgets.QRadioButton(self.gridLayoutWidget)
        self.radioButton_tithi.setObjectName("radioButton_tithi")
        self.horizontalLayout_seva_date_basis.addWidget(self.radioButton_tithi)
        self.radioButton_flexible = QtWidgets.QRadioButton(self.gridLayoutWidget)
        self.radioButton_flexible.setObjectName("radioButton_flexible")
        self.horizontalLayout_seva_date_basis.addWidget(self.radioButton_flexible)




        self.gridLayout.addLayout(self.horizontalLayout_seva_date_basis, 6, 2, 1, 1)
        self.label_seva_start = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_seva_start.setObjectName("label_seva_start")
        self.gridLayout.addWidget(self.label_seva_start, 5, 0, 1, 1)
        self.verticalLayout_date_preference = QtWidgets.QVBoxLayout()
        self.verticalLayout_date_preference.setObjectName("verticalLayout_date_preference")
        self.spinBox_date = QtWidgets.QSpinBox(self.gridLayoutWidget)
        self.spinBox_date.setObjectName("spinBox_date")
        self.verticalLayout_date_preference.addWidget(self.spinBox_date)
        self.comboBox_nakshatra_2 = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.comboBox_nakshatra_2.setObjectName("comboBox_nakshatra_2")
        self.verticalLayout_date_preference.addWidget(self.comboBox_nakshatra_2)
        self.horizontalLayout_day_week_no = QtWidgets.QHBoxLayout()
        self.horizontalLayout_day_week_no.setObjectName("horizontalLayout_day_week_no")
        self.label_day = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_day.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_day.setObjectName("label_day")
        self.horizontalLayout_day_week_no.addWidget(self.label_day)
        self.comboBox_day = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.comboBox_day.setObjectName("comboBox_day")
        self.horizontalLayout_day_week_no.addWidget(self.comboBox_day)
        self.label_week = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_week.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_week.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_week.setObjectName("label_week")
        self.horizontalLayout_day_week_no.addWidget(self.label_week)
        self.spinBox_week_no = QtWidgets.QSpinBox(self.gridLayoutWidget)
        self.spinBox_week_no.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.spinBox_week_no.setMinimum(1)
        self.spinBox_week_no.setMaximum(6)
        self.spinBox_week_no.setProperty("value", 1)
        self.spinBox_week_no.setObjectName("spinBox_week_no")
        self.horizontalLayout_day_week_no.addWidget(self.spinBox_week_no)
        self.horizontalLayout_day_week_no.setStretch(1, 1)
        self.horizontalLayout_day_week_no.setStretch(3, 1)
        self.verticalLayout_date_preference.addLayout(self.horizontalLayout_day_week_no)
        self.comboBox_tithi = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.comboBox_tithi.setObjectName("comboBox_tithi")
        self.verticalLayout_date_preference.addWidget(self.comboBox_tithi)


        self.gridLayout.addLayout(self.verticalLayout_date_preference, 7, 2, 1, 1)
        self.comboBox_nakshatra = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.comboBox_nakshatra.setObjectName("comboBox_nakshatra")
        self.gridLayout.addWidget(self.comboBox_nakshatra, 3, 2, 1, 1)
        self.label_rashi = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_rashi.setObjectName("label_rashi")
        self.gridLayout.addWidget(self.label_rashi, 2, 0, 1, 1)
        self.comboBox_rashi = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.comboBox_rashi.setObjectName("comboBox_rashi")
        self.gridLayout.addWidget(self.comboBox_rashi, 2, 2, 1, 1)
        self.label_gotra = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_gotra.setObjectName("label_gotra")
        self.gridLayout.addWidget(self.label_gotra, 4, 0, 1, 1)
        self.label_gender = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_gender.setObjectName("label_gender")
        self.gridLayout.addWidget(self.label_gender, 1, 0, 1, 1)
        self.comboBox_gender = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.comboBox_gender.setObjectName("comboBox_gender")
        self.gridLayout.addWidget(self.comboBox_gender, 1, 2, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1079, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.seva_date_basis.addButton(self.radioButton_date)
        self.seva_date_basis.addButton(self.radioButton_nakshatra)
        self.seva_date_basis.addButton(self.radioButton_week)
        self.seva_date_basis.addButton(self.radioButton_tithi)
        self.seva_date_basis.addButton(self.radioButton_flexible)

        self.seva_group_yesorno.addButton(self.radioButton_group_yes)
        self.seva_group_yesorno.addButton(self.radioButton_group_no)

        self.radioButton_group_yes.toggled.connect(self.group_address_handling)
        # self.radioButton_group_no.toggled.connect(self.address_handling)



        # self.

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_date.setText(_translate("MainWindow", "Seva date preference"))
        self.label_start_month.setText(_translate("MainWindow", "Month"))
        self.label_star_year.setText(_translate("MainWindow", "Year"))
        self.label_nakshatra.setText(_translate("MainWindow", "Nakshatra"))
        self.label_name.setText(_translate("MainWindow", "Name"))
        self.label_group.setText(_translate("MainWindow", "Does this sevadar belong to a group?"))
        self.label_basis.setText(_translate("MainWindow", "Seva date basis"))
        self.label_address.setText(_translate("MainWindow", "Address"))
        self.radioButton_group_yes.setText(_translate("MainWindow", "Yes"))
        self.radioButton_group_no.setText(_translate("MainWindow", "No"))
        self.radioButton_date.setText(_translate("MainWindow", "Date"))
        self.radioButton_nakshatra.setText(_translate("MainWindow", "Nakshatra"))
        self.radioButton_week.setText(_translate("MainWindow", "Week number and day"))
        self.radioButton_tithi.setText(_translate("MainWindow", "Tithi"))
        self.radioButton_flexible.setText(_translate("MainWindow", "Flexible"))
        self.label_seva_start.setText(_translate("MainWindow", "Seva start"))
        self.label_day.setText(_translate("MainWindow", "Day"))
        self.label_week.setText(_translate("MainWindow", "Week number"))
        self.label_rashi.setText(_translate("MainWindow", "Rashi"))
        self.label_gotra.setText(_translate("MainWindow", "Gotra"))
        self.label_gender.setText(_translate("MainWindow", "Gender"))




    def group_address_handling(self,selected):
        if selected:
            self.verticalLayout_address = QtWidgets.QVBoxLayout()
            self.verticalLayout_address.setObjectName("verticalLayout_address")
            self.comboBox_address = QtWidgets.QComboBox(self.gridLayoutWidget)
            self.comboBox_address.setObjectName("comboBox_address")
            self.verticalLayout_address.addWidget(self.comboBox_address)
        else:
            # self.gridLayout.removeItem(self.verticalLayout_address)
            self.verticalLayout_address = QtWidgets.QVBoxLayout()
            self.verticalLayout_address.setObjectName("verticalLayout_address")
            self.lineEdit_address1 = QtWidgets.QLineEdit(self.gridLayoutWidget)
            self.lineEdit_address1.setObjectName("lineEdit_address1")
            self.verticalLayout_address.addWidget(self.lineEdit_address1)
            self.lineEdit_address2 = QtWidgets.QLineEdit(self.gridLayoutWidget)
            self.lineEdit_address2.setObjectName("lineEdit_address2")
            self.verticalLayout_address.addWidget(self.lineEdit_address2)
            self.lineEdit_address3 = QtWidgets.QLineEdit(self.gridLayoutWidget)
            self.lineEdit_address3.setObjectName("lineEdit_address3")
            self.verticalLayout_address.addWidget(self.lineEdit_address3)
            self.lineEdit_address4 = QtWidgets.QLineEdit(self.gridLayoutWidget)
            self.lineEdit_address4.setObjectName("lineEdit_address4")
            self.verticalLayout_address.addWidget(self.lineEdit_address4)
            # self.verticalLayout_address.addLayout(self.verticalLayout_address)
        
        self.gridLayout.addLayout(self.verticalLayout_address, 9, 2, 1, 1)
        # self.gridLayout.removeItem(self.verticalLayout_address)

        



        self.verticalLayout_address.setEnabled(False)

    


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


import sqlite3
from sqlite3.dbapi2 import DataError
import sys

from PyQt5 import QtCore
from assign_dates import assign_dates
from pdf import create_pdf

from PyQt5.QtWidgets import QApplication, QHeaderView, QLabel, QPushButton, QScrollArea, QTableWidget, QVBoxLayout, QWidget

from calendar import monthcalendar
from shutil import copyfile
from datetime import datetime


class App(QWidget):
    def __init__(self,year,month):
        super().__init__()
        self.title = str(month)+'-'+str(year)+' Calendar overview'
        self.left = 0
        self.top = 0
        self.width = 1000
        self.height = 500
   
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
   
        self.year = year
        self.month = month
        self.createTable()
   
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tableWidget)
        self.setLayout(self.layout)
   
        #Show window
        self.show()

   
    #Create table
    def createTable(self):

        mon_cal = monthcalendar(2021,9)
        self.tableWidget = QTableWidget()
  
        #Row count
        self.tableWidget.setRowCount(len(mon_cal))

        #Column count
        self.tableWidget.setColumnCount(8)
        self.tableWidget.setHorizontalHeaderLabels(('Mon','Tue','Wen','Thu','Fri','Sat','Sun',''))


        bold_font = self.tableWidget.font()
        bold_font.setBold(True)

        self.assigned_dates = assign_dates('data\Seva_manager.db',self.year,self.month)
        print(self.assigned_dates)

        try:
            con = sqlite3.connect('data\Seva_manager.db')
            cur = con.cursor()
            for week_no, week in enumerate(mon_cal):
                for day,date in enumerate(week):
                    if date != 0:
                        # w = QWidget(QVBoxLayout)
                        # layout = QWidget()                    
                        # date_label = QLabel()
                        # date_label.setText(str(date))
                        # layout.addWidget(date_label)
                        text =str(date)#+'\n'


                        for i in self.assigned_dates[date]:
                            cur.execute(f"select name from Sevadars where sevadar_id = {i}")
                            text += '\n'+cur.fetchone()[0]
                        tabledata = QLabel()
                        tabledata.setText(text)
                        tabledata.setAlignment(QtCore.Qt.AlignLeft)
                        # scroll.addScrollBarWidget(tabledata)
                        # t.addWidget(scroll)
                        self.tableWidget.setCellWidget(week_no,day,tabledata)        
        except Exception as e:
            print(e)
        finally:
            con.close()

        download_button = QPushButton(text='Create PDF')
        download_button.clicked.connect(self.download_callback)
        self.tableWidget.setCellWidget(2,7,download_button)
        self.tableWidget.setSpan(0,7,7,1)
        
        self.tableWidget.verticalHeader().hide()
        
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def download_callback(self):
        create_pdf(self.year,self.month,self.assigned_dates)
        now = datetime.now()
        fname = f'backup\{now.strftime("%d_%m_%Y_%H_%M")}_BACKUP_DB_{str(self.month)}_{str(self.year)}.db'
        copyfile('data\Seva_manager.db',fname)
        print("Back up done", fname)

if __name__ == "__main__":
    global app
    app = QApplication(sys.argv)
    global ex
    year,month = 2021,1
    ex = App(year,month)
    sys.exit(app.exec())
import sqlite3

from PyQt5 import QtCore
from assign_dates import assign_dates
import sys
from PyQt5.QtWidgets import QApplication, QGridLayout, QHeaderView, QLabel, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget

from calendar import monthcalendar


class App(QWidget):
    def __init__(self,year,month):
        super().__init__()
        self.title = 'PyQt5 - QTableWidget'
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
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels(('Mon','Tue','Wen','Thu','Fri','Sat','Sun'))


        bold_font = self.tableWidget.font()
        bold_font.setBold(True)

        assigned_dates = assign_dates('data\Seva_manager.db',self.year,self.month)
        print(assigned_dates)

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
                        text =str(date)+'\n'


                        for i in assigned_dates[date]:
                            cur.execute(f"select name from Sevadars where sevadar_id = {i}")
                            text += '\n'+cur.fetchone()[0]
                            
                        # layout.addWidget(tabledata)
                        # w.
                        tabledata = QLabel()
                        tabledata.setText(text)
                        tabledata.setAlignment(QtCore.Qt.AlignLeft)
                        self.tableWidget.setCellWidget(week_no,day,tabledata)        
        except Exception as e:
            print(e)
        finally:
            con.close()
        
        self.tableWidget.verticalHeader().hide()
        
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)




def overview(year,month):
    global app
    app = QApplication(sys.argv)
    global ex
    ex = App(year,month)
    sys.exit(app.exec())
overview(2021,9)
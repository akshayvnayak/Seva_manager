import time
import sys
from PyQt5.QtCore import QCoreApplication
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

#Main Window
class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 - QTableWidget'
        self.left = 0
        self.top = 0
        self.width = 600
        self.height = 600

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.createTable()

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tableWidget)
        self.setLayout(self.layout)

        self.show()

    def createTable(self):
        self.tableWidget = QTableWidget()
        # self.tableWidget.setModel(model)


        try:
            conn = sqlite3.connect('data\Seva_manager.db')
            conn.row_factory = dict_factory
            print("Opened database successfully")
            cur = conn.cursor()
            cur.execute(f"""
                select * from sevadardetails;
            """)
            sevadars_details = cur.fetchall()
        except Exception as e:
            print(format_exc())
        finally:
            conn.close()
        
        #Row count
        self.tableWidget.setRowCount(len(sevadars_details))
        # print(sevadars_details)
        

        #Column count
        self.tableWidget.setColumnCount(13)
        self.tableWidget.setHorizontalHeaderLabels(['Id','Name','Rashi','Nakshatra','Gotra','Seva Date basis','Preferred date','Start month','Flexible','Group id','Address'])


        for i,s in enumerate(sevadars_details):
            self.tableWidget.setItem(i,0,QTableWidgetItem(str(s['sevadar_id'])))
            self.tableWidget.setItem(i,1,QTableWidgetItem(s['name']))
            self.tableWidget.setItem(i,2,QTableWidgetItem(sknames.rashis[str(s['rashi'])]))
            self.tableWidget.setItem(i,3,QTableWidgetItem(sknames.nakshatras[str(s['nakshatra'])]))
            self.tableWidget.setItem(i,4,QTableWidgetItem(sknames.gotras[str(s['gotra'])]))
            self.tableWidget.setItem(i,5,QTableWidgetItem(sknames.pooja_basis[(s['pooja_basis'])]))
            
            pooja_date =    (str(s['pooja_date']) if (s['pooja_basis']==0) else 
                            sknames.nakshatras[str(s['pooja_date'])] if s['pooja_basis'] == 1 else
                            'Week '+ str(s['pooja_date'])[0] + ' : ' + sknames.vaaras[str(s['pooja_date'])[1]] if s['pooja_basis'] == 2 else
                            sknames.tithis[str(s['pooja_date'])])
                

            self.tableWidget.setItem(i,6,QTableWidgetItem(pooja_date))
            self.tableWidget.setItem(i,7,QTableWidgetItem(s['start_yyyymm']))
            self.tableWidget.setItem(i,8,QTableWidgetItem('YES' if s['flexible'] else 'NO'))
            self.tableWidget.setItem(i,9,QTableWidgetItem('YES' if s['group_id'] else 'NO'))

            self.tableaddress = QLabel()
            self.tableaddress.setText(s['line1']+'\n'+s['line2']+'\n'+s['line3']+'\n'+s['line4'])
            self.tableWidget.setCellWidget(i,10,self.tableaddress)
            # self.tableWidget.setItem(i,10,QTableWidgetItem(s['line1']+'\n'+s['line2']+'\n'+s['line3']+'\n'+s['line4']))
            self.tableWidget.setItem(i,11,QTableWidgetItem(type=2))
            edit_button = QPushButton()
            edit_button.setText('EDIT')
            edit_button.clicked.connect(lambda x, sevadar_id = s['sevadar_id'] : self.edit_button_callback(sevadar_id))
            self.tableWidget.setCellWidget(i,11,edit_button)
        

        self.tableWidget.resizeRowsToContents()
        self.tableWidget.resizeColumnsToContents()

        #Table will fit the screen horizontally
        # self.tableWidget.horizontalHeader().setStretchLastSection(True)
        # self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def edit_button_callback(self, sevadar_id):
        # QApplication.closeAllWindows()
        # global ex
        print('asdf')
        # global app
        # app.quit()
        # import time
        # time.sleep(5)
        edit_sevadar_page.edit_sevadar(sevadar_id)
        # print(format_exc())



def display_sevadars():
        global app
        app = QApplication(sys.argv)
        global ex
        ex = App()
        sys.exit(app.exec())

display_sevadars()
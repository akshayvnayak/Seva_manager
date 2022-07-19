import sys
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
        # self.tableWidget.setModel(model)


        try:
            conn = sqlite3.connect('data\Seva_manager.db')
            conn.row_factory = dict_factory
            print("Opened database successfully")
            cur = conn.cursor()
            cur.execute("PRAGMA foreign_keys=ON")
            conn.commit()
            cur.execute(f"""
                select * from sevadardetailsRecent;
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
            self.tableWidget.setItem(i,9,QTableWidgetItem(str(s['group_id'])))

            self.tableaddress = QLabel()
            self.tableaddress.setText(s['line1']+'\n'+s['line2']+'\n'+s['line3']+'\n'+s['line4'])
            self.tableWidget.setCellWidget(i,10,self.tableaddress)
            # self.tableWidget.setItem(i,10,QTableWidgetItem(s['line1']+'\n'+s['line2']+'\n'+s['line3']+'\n'+s['line4']))
            self.tableWidget.setItem(i,11,QTableWidgetItem(type=2))
            edit_button = QPushButton()
            edit_button.setText('EDIT')
            edit_button.clicked.connect(lambda x, sevadar_id = s['sevadar_id'] : self.edit_button_callback(sevadar_id))
            self.tableWidget.setCellWidget(i,11,edit_button)

            
            self.tableWidget.setItem(i,12,QTableWidgetItem(type=2))
            delete_button = QPushButton()
            delete_button.setText('DELETE')
            delete_button.clicked.connect(lambda x, sevadar_id = s['sevadar_id'] : self.show_delete_popup(sevadar_id))
            self.tableWidget.setCellWidget(i,12,delete_button)
            
        

        self.tableWidget.resizeRowsToContents()
        self.tableWidget.resizeColumnsToContents()

        self.tableWidget.verticalHeader().hide()
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
        edit_sevadar_page.edit_sevadar(sevadar_id,self)
        # print(format_exc())


    def show_delete_popup(self,s_id):
        msg = QMessageBox()
        msg.setWindowTitle("Warning!")
        msg.setText("Are you sure want to delete it?")
        msg.setIcon(QMessageBox.Critical)
        msg.setStandardButtons(QMessageBox.Cancel|QMessageBox.Ok)
        msg.setDefaultButton(QMessageBox.Cancel)
        msg.setInformativeText("This will delete all the data of the sevadar!")

        msg.buttonClicked.connect(lambda x, s = s_id: self.delete_popup_callback(x,s))
        # msg.buttonClicked.connect(lambda x : print(x.int()))

        x = msg.exec_()

    def delete_popup_callback(self,response,s_id):
        if response.text() == 'Cancel':
            return
        try:
            conn = sqlite3.connect('data\Seva_manager.db')
            print("Opened database successfully", __name__)
            cur = conn.cursor()
            cur.execute("PRAGMA foreign_keys=ON")
            conn.commit()
            cur.execute(f"""
                DELETE FROM Sevadars WHERE sevadar_id = {s_id};
            """)
            conn.commit()
            # print(cur.fetchall())
            # self.sevadar= cur.fetchone()
        except Exception as e:
            print(format_exc())
        finally:
            conn.close()
        print(s_id,"deleted")
        self.close()
        ex = App()


if __name__ == '__main__':
        global app
        app = QApplication(sys.argv)
        global ex
        ex = App()
        sys.exit(app.exec())
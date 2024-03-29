from msilib.schema import Icon
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
import sqlite3
from traceback import format_exc
import SanskritNames as sknames
import edit_sevadar_page


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

# Main Window


class App(QWidget):
    def __init__(self):
        super().__init__()

        self.default_font = QFont()
        self.default_font.setPointSize(13)

        self.setFont(self.default_font)
        self.title = 'Sevadars List'
        self.left = 0
        self.top = 0
        self.width = 1200
        self.height = 720

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.createTable()

        self.layout = QVBoxLayout()
        self.edit = QLineEdit()
        self.edit.textChanged.connect(self.filter)
        self.layout.addWidget(self.edit)
        self.layout.addWidget(self.tableWidget)
        self.setLayout(self.layout)

        self.showMaximized()

    def filter(self, filter_text):
        for i in range(self.tableWidget.rowCount()):
            for j in range(self.tableWidget.columnCount()):
                if (j == 10):
                    item = self.tableWidget.cellWidget(i, j)
                else:
                    item = self.tableWidget.item(i, j)
                match = filter_text.lower() not in item.text().lower()
                self.tableWidget.setRowHidden(i, match)
                if not match:
                    break

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

        # Row count
        self.tableWidget.setRowCount(len(sevadars_details))
        # print(sevadars_details)

        # Column count
        self.tableWidget.setColumnCount(14)
        self.tableWidget.setHorizontalHeaderLabels(
            ['Id', 'Name', 'Rashi', 'Nakshatra', 'Gotra', 'Seva Date basis', 'Preferred date', 'Start month', 'Flexible', 'Group id', 'Address', "", '', ''])
        # self.default_font.setBold(True)
        self.default_font.setCapitalization(True)
        self.default_font.setBold(True)
        self.tableWidget.horizontalHeader().setFont(self.default_font)

        for i, s in enumerate(sevadars_details):
            self.tableWidget.setItem(
                i, 0, QTableWidgetItem(str(s['sevadar_id'])))
            self.tableWidget.setItem(i, 1, QTableWidgetItem(s['name']))
            self.tableWidget.setItem(i, 2, QTableWidgetItem(
                sknames.rashis[str(s['rashi'])]))
            self.tableWidget.setItem(i, 3, QTableWidgetItem(
                sknames.nakshatras[str(s['nakshatra'])]))
            self.tableWidget.setItem(i, 4, QTableWidgetItem(
                sknames.gotras[str(s['gotra'])]))
            self.tableWidget.setItem(i, 5, QTableWidgetItem(
                sknames.pooja_basis[(s['pooja_basis'])]))

            pooja_date = (str(s['pooja_date']) if (s['pooja_basis'] == 0) else
                          sknames.nakshatras[str(s['pooja_date'])] if s['pooja_basis'] == 1 else
                          'Week ' + str(s['pooja_date'])[0] + ' : ' + sknames.vaaras[str(s['pooja_date'])[1]] if s['pooja_basis'] == 2 else
                          sknames.tithis[str(s['pooja_date'])])

            self.tableWidget.setItem(i, 6, QTableWidgetItem(pooja_date))
            self.tableWidget.setItem(i, 7, QTableWidgetItem(s['start_yyyymm']))
            self.tableWidget.setItem(i, 8, QTableWidgetItem(
                'YES' if s['flexible'] else 'NO'))

            ############################################# To make it simple, displaying address_id rather than group_id ##################
            self.tableWidget.setItem(i, 9, QTableWidgetItem(
                str(s['address_id'] if s["group_id"] else "NA")))  # group_id

            self.tableaddress = QLabel()
            self.tableaddress.setText(
                s['line1']+'\n'+s['line2']+'\n'+s['line3']+'\n'+s['line4'])
            self.tableaddress.setMargin(10)
            self.tableWidget.setCellWidget(i, 10, self.tableaddress)
            # self.tableWidget.setItem(i,10,QTableWidgetItem(s['line1']+'\n'+s['line2']+'\n'+s['line3']+'\n'+s['line4']))
            self.tableWidget.setItem(i, 11, QTableWidgetItem(type=2))
            edit_button = QPushButton()
            edit_button.setText('EDIT')
            edit_button.clicked.connect(
                lambda x, sevadar_id=s['sevadar_id']: self.edit_button_callback(sevadar_id))
            self.tableWidget.setCellWidget(i, 11, edit_button)

            self.tableWidget.setItem(i, 12, QTableWidgetItem(type=2))
            delete_button = QPushButton()
            delete_button.setText('DELETE SEVADAR')
            delete_button.clicked.connect(
                lambda x, s_id=s['sevadar_id'], sevadar_name=s['name']: self.show_delete_popup(s_id, sevadar_name))
            self.tableWidget.setCellWidget(i, 12, delete_button)

            self.tableWidget.setItem(i, 13, QTableWidgetItem(type=2))
            delete_recent_renewal_button = QPushButton()
            delete_recent_renewal_button.setText('DELETE RECENT RENEWAL')
            delete_recent_renewal_button.clicked.connect(
                lambda x, s_id=s['sevadar_id'], sevadar_name=s['name'], yyyymm=s['start_yyyymm']: self.show_delete_renewal_popup(s_id, sevadar_name, yyyymm))
            self.tableWidget.setCellWidget(i, 13, delete_recent_renewal_button)

        self.tableWidget.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeToContents)
        self.tableWidget.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        self.tableWidget.setContentsMargins(50, 5, 5, 5)

        # self.tableWidget.setStyleSheet("QTableWidget { padding: 5px ; }")

        self.tableWidget.verticalHeader().hide()
        # Table will fit the screen horizontally
        # self.tableWidget.horizontalHeader().setStretchLastSection(True)
        # self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def edit_button_callback(self, sevadar_id):
        # QApplication.closeAllWindows()
        # global ex
        print('edit', sevadar_id)
        # global app
        # app.quit()
        # import time
        # time.sleep(5)
        edit_sevadar_page.edit_sevadar(sevadar_id, self)
        # print(format_exc())

    def show_delete_popup(self, s_id, s_name):
        msg = QMessageBox()
        self.default_font.setCapitalization(False)
        msg.setFont(self.default_font)
        msg.setWindowTitle("WARNING!")
        msg.setText(s_name)
        msg.setIcon(QMessageBox.Critical)
        msg.setStandardButtons(QMessageBox.Cancel | QMessageBox.Ok)
        msg.setDefaultButton(QMessageBox.Cancel)
        msg.setInformativeText(
            "Are you sure want to delete? \nThis will delete all the data of this sevadar!")
        msg.buttonClicked.connect(
            lambda x, s=s_id: self.delete_popup_callback(x, s))
        # msg.buttonClicked.connect(lambda x : print(x.int()))

        x = msg.exec_()

    def delete_popup_callback(self, response, s_id):
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
        print(s_id, "deleted")
        self.close()
        ex = App()

    def show_delete_renewal_popup(self, s_id, s_name, yyyymm):
        msg = QMessageBox()
        self.default_font.setCapitalization(False)
        msg.setFont(self.default_font)
        msg.setWindowTitle("WARNING!")
        msg.setText(s_name)
        msg.setIcon(QMessageBox.Critical)
        msg.setStandardButtons(QMessageBox.Cancel | QMessageBox.Ok)
        msg.setDefaultButton(QMessageBox.Cancel)
        msg.setInformativeText(
            "Are you sure want to delete recent renewal " + yyyymm + " of " + s_name)
        msg.buttonClicked.connect(
            lambda x, s_id=s_id, s_yyyymm=yyyymm: self.delete_renewal_popup_callback(x, s_id, s_yyyymm))
        # msg.buttonClicked.connect(lambda x : print(x.int()))

        x = msg.exec_()

    def delete_renewal_popup_callback(self, response, s_id, s_yyyymm):
        if response.text() == 'Cancel':
            return
        try:
            conn = sqlite3.connect('data\Seva_manager.db')
            print("Opened database successfully", __name__)
            cur = conn.cursor()
            cur.execute("PRAGMA foreign_keys=ON")
            conn.commit()
            cur.execute(f"""
                DELETE FROM SevaStartMonths 
                WHERE sevadar_id = {s_id} AND start_yyyymm = '{s_yyyymm}';
            """)
            conn.commit()
            print(f"""
                DELETE FROM SevaStartMonths 
                WHERE sevadar_id = {s_id} AND start_yyyymm = '{s_yyyymm}';
            """)
            # print(cur.fetchall())
            # self.sevadar= cur.fetchone()
        except Exception as e:
            print(format_exc())
        finally:
            conn.close()
        print(s_id, "deleted")
        self.close()
        ex = App()


if __name__ == '__main__':
    global app
    app = QApplication(sys.argv)
    global ex
    ex = App()
    sys.exit(app.exec())

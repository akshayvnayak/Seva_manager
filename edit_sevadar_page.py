from collections import namedtuple
import sqlite3
from tokenize import group
from traceback import format_exc
import traceback
from PyQt5 import QtWidgets
from add_sevadar_page import Ui_MainWindow, dict_factory
import display_sevadars


class Ui (Ui_MainWindow):
    def __init__(self, window, s_id):
        # print('s_id',s_id)
        super().__init__(window)
        self.setup(s_id)

    def setup(self, s_id):
        self.s_id = s_id
        # sevadar = {}
        try:
            conn = sqlite3.connect('data\Seva_manager.db')
            conn.row_factory = dict_factory
            print("Opened database successfully", __name__)
            cur = conn.cursor()
            cur.execute("PRAGMA foreign_keys=ON")
            conn.commit()
            cur.execute(f"""
                select * from sevadardetailsRecent where sevadar_id = {s_id};
            """)
            self.sevadar = cur.fetchone()
            # print(sevadar)
            # x = self.sevadar
            # print(self.sevadar)
        except Exception as e:
            print(format_exc())
        finally:
            conn.close()
        # self.sevadar = sevadar
        print(self.sevadar)
        self.set_selected_options()

    def set_selected_options(self):
        self.lineEdit_name.setText(self.sevadar['name'])
        self.comboBox_rashi.setCurrentIndex(self.sevadar['rashi']-1)
        self.comboBox_nakshatra.setCurrentIndex(self.sevadar['nakshatra']-1)
        self.comboBox_gotra.setCurrentIndex(self.sevadar['gotra']-1)
        self.comboBox_start_month.setCurrentIndex(
            int(self.sevadar['start_yyyymm'][-2:])-1)
        self.spinBox_start_year.setValue(int(self.sevadar['start_yyyymm'][:4]))
        self.radioButton_date_basis[self.sevadar['pooja_basis']].click()

        # "date":(self.spinBox_date.value(),
        #             self.comboBox_nakshatra_2.currentIndex()+1,
        #             self.spinBox_week_no.value()*10+self.comboBox_day.currentIndex(),
        #             self.comboBox_tithi.currentIndex()+1),

        p = self.sevadar['pooja_basis']
        if p == 0:
            self.spinBox_date.setValue(self.sevadar['pooja_date'])
        elif p == 1:
            self.comboBox_nakshatra_2.setCurrentIndex(
                self.sevadar['pooja_date']-1)
        elif p == 2:
            self.spinBox_week_no.setValue(self.sevadar['pooja_date']//10)
            self.comboBox_day.setCurrentIndex(self.sevadar['pooja_date'] % 10)
        else:
            self.comboBox_tithi.setCurrentIndex(self.sevadar['pooja_date']-1)
        self.checkBox_flexible.setChecked(self.sevadar['flexible'])

        self.radioButton_existing_address.click()
        self.comboBox_address.setCurrentIndex(self.sevadar['address_id']-1)

        self.radioButton_group_no.setChecked(self.sevadar['group_id'] == None)

        self.buttonBox.accepted.disconnect()
        self.buttonBox.accepted.connect(
            lambda s_id=self.s_id: edit_sevadar_callback(
                s_id,
                self.sevadar,
                {
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
                }
            )
        )


def edit_sevadar_callback(s_id, prev_sevadar, sevadar_details_dict):
    global MainWindow
    MainWindow.close()
    global ex
    ex.close()
    # ex = display_sevadars.App()
    sevadar_details = namedtuple("SevadarDetails", sevadar_details_dict.keys())(
        *sevadar_details_dict.values())
    print('previous', prev_sevadar)
    print(sevadar_details)
    try:
        conn = sqlite3.connect('data\Seva_manager.db')
        # conn.row_factory = dict_factory
        print("Opened database successfully", __name__)
        cur = conn.cursor()
        cur.execute("PRAGMA foreign_keys=ON")
        conn.commit()
        cur.execute(f"""
            UPDATE Sevadars
            SET name = "{sevadar_details.name}",
                rashi = {sevadar_details.rashi},
                nakshatra = {sevadar_details.nakshatra},
                gotra = {sevadar_details.gotra},
                pooja_basis  = {sevadar_details.date_basis},
                pooja_date = {sevadar_details.date[sevadar_details.date_basis]}
            WHERE sevadar_id = {s_id};
        """)
        conn.commit()
        # cur.execute('SELECT last_insert_rowid()')
        # sevadar_id = cur.fetchone()[0]
        # print(sevadar_id)
        cur.execute(
            f"SELECT * from SevadarsFlexible WHERE sevadar_id = {s_id};")

        # print('flexible',)
        if sevadar_details.flexible_flag:
            if cur.fetchone() == None:
                cur.execute(f"INSERT INTO SevadarsFlexible VALUES ({s_id})")
        else:
            if cur.fetchone() != None:
                cur.execute(
                    f"DELETE FROM SevadarsFlexible WHERE sevadar_id = {s_id}")

        cur.execute(f"""
            UPDATE SevaStartMonths
            SET start_yyyymm = '{sevadar_details.start_month}'
            WHERE sevadar_id = {s_id}
                AND start_yyyymm = (select start_yyyymm from SevaStartMonths where sevadar_id = {s_id});
        """)
        # conn.commit()

        address_id = sevadar_details.address_id
        if sevadar_details.new_address_flag:
            cur.execute(f"""
                INSERT INTO Addresses (line1,line2,line3,line4)
                VALUES('{sevadar_details.address[0]}','{sevadar_details.address[1]}','{sevadar_details.address[2]}','{sevadar_details.address[3]}');
            """)
            conn.commit()
            cur.execute('SELECT last_insert_rowid()')
            address_id = cur.fetchone()[0]

        # or sevadar_details.group_flag != None:
        if sevadar_details.group_flag != (prev_sevadar['group_id'] != None):
            if sevadar_details.group_flag:
                conn.commit()
                cur.execute(
                    f"DELETE FROM SevadarAddress WHERE sevadar_id = {s_id}")
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
                    VALUES({s_id},{group_id})
                ''')

                cur.execute(
                    f"DELETE FROM SevadarAddress WHERE sevadar_id = {s_id}")

            else:
                cur.execute(f"""
                    INSERT INTO SevadarAddress
                    VALUES({s_id},{address_id});
                """)
                cur.execute(f"DELETE FROM Groups WHERE sevadar_id = {s_id}")

        else:
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
                    UPDATE Groups
                    SET group_id = {group_id}
                    WHERE sevadar_id = {s_id};
                ''')

                cur.execute(
                    f"DELETE FROM SevadarAddress WHERE sevadar_id = {s_id}")

            else:
                cur.execute(f"""
                    UPDATE SevadarAddress
                    SET address_id = {address_id}
                    WHERE sevadar_id = {s_id};
                """)
                cur.execute(f"DELETE FROM Groups WHERE sevadar_id = {s_id}")

        conn.commit()
    except Exception as e:
        print("Database error:", e)
        print(traceback.format_exc())
    finally:
        conn.close()
    ui.close()
    # global ex
    # ex.close()
    ex = display_sevadars.App()


def edit_sevadar(s_id, window):
    # import sys
    # app = QtWidgets.QApplication(sys.argv)
    global MainWindow
    MainWindow = QtWidgets.QMainWindow()
    global ui
    ui = Ui(MainWindow, s_id)
    MainWindow.setWindowTitle("Edit Sevadar")
    MainWindow.showMaximized()
    global ex
    ex = window
    # return MainWindow
    # app.exec()

# edit_sevadar(5)

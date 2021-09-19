import sqlite3
from sqlite3.dbapi2 import Error

try:
    conn = sqlite3.connect('data\Seva_manager.db')
    print("Opened database successfully")
    cur = conn.cursor()
    cur.execute(
        '''
            CREATE TABLE IF NOT EXISTS Sevadars(
                sevadar_id  INTEGER PRIMARY KEY AUTOINCREMENT,
                name        TEXT,
                rashi       INTEGER,
                nakshatra   INTEGER,
                gotra       INTEGER,
                pooja_basis INTEGER,
                pooja_date  INTEGER
            );
        '''
    )
    conn.commit()
    cur.execute(
        '''
            CREATE TABLE IF NOT EXISTS Addresses(
                address_id  INTEGER PRIMARY KEY AUTOINCREMENT,
                line1       TEXT,
                line2       TEXT,
                line3       TEXT,
                line4       TEXT
            );
        '''
    )
    conn.commit()
    cur.execute(
        '''
            CREATE TABLE IF NOT EXISTS GroupDetails(
                group_id    INTEGER PRIMARY KEY AUTOINCREMENT,
                address_id  INTEGER,
                FOREIGN KEY(address_id)
                    REFERENCES Addresses(address_id)
                        ON UPDATE CASCADE
                        ON DELETE CASCADE
            );
        '''
    )
    conn.commit()
    cur.execute(
        '''
            CREATE TABLE IF NOT EXISTS Groups(
                sevadar_id  INTEGER,
                group_id    INTEGER,
                FOREIGN KEY(group_id)
                    REFERENCES GroupDetails(group_id)
                        ON UPDATE CASCADE
                        ON DELETE CASCADE,
                FOREIGN KEY(sevadar_id)
                    REFERENCES Sevadars(sevadar_id)
                        ON UPDATE CASCADE
                        ON DELETE CASCADE
            );
        '''
    )
    conn.commit()
    cur.execute(
        '''
            CREATE TABLE IF NOT EXISTS SevadarAddress(
                sevadar_id  INTEGER,
                address_id  INTEGER,
                FOREIGN KEY(sevadar_id)
                    REFERENCES Sevadars(sevadar_id)
                        ON UPDATE CASCADE
                        ON DELETE CASCADE,
                FOREIGN KEY(address_id)
                    REFERENCES Addresses(address_id)
                        ON UPDATE CASCADE
                        ON DELETE CASCADE
            );
        '''
    )
    conn.commit()
    cur.execute(
        '''
            CREATE TABLE IF NOT EXISTS SevaStartMonths(
                sevadar_id INTEGER,
                start_yyyymm TEXT,
                FOREIGN KEY (sevadar_id)
                    REFERENCES Sevadars(sevadar_id)
                        ON UPDATE CASCADE
                        ON DELETE CASCADE
            );
        '''
    )
    conn.commit()
    cur.execute(
        '''
            CREATE TABLE IF NOT EXISTS SevadarsFlexible(
                sevadar_id          INTEGER,
                FOREIGN KEY (sevadar_id)
                    REFERENCES Sevadars(sevadar_id)
                        ON UPDATE CASCADE
                        ON DELETE CASCADE
            );
        '''
    )
    conn.commit()
    cur.execute(
        '''
            CREATE TABLE IF NOT EXISTS PoojaCount(
                yyyymm  TEXT,
                count INTEGER
            );
        '''
    )
    conn.commit()
except Error as e:
    print('SQLite Error:',e)
finally:
    conn.close()

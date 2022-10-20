import sqlite3
from sqlite3.dbapi2 import Error

try:
    conn = sqlite3.connect('data\Seva_manager.db')
    print("Opened database successfully")
    cur = conn.cursor()
    cur.executescript(
        '''
            --
            -- File generated with SQLiteStudio v3.3.3 on Thu Oct 20 21:27:38 2022
            --
            -- Text encoding used: System
            --
            PRAGMA foreign_keys = off;
            BEGIN TRANSACTION;

            -- Table: Addresses
            DROP TABLE IF EXISTS Addresses;

            CREATE TABLE Addresses (
                address_id INTEGER PRIMARY KEY AUTOINCREMENT,
                line1      TEXT,
                line2      TEXT,
                line3      TEXT,
                line4      TEXT
            );


            -- Table: GroupDetails
            DROP TABLE IF EXISTS GroupDetails;

            CREATE TABLE GroupDetails (
                group_id   INTEGER PRIMARY KEY AUTOINCREMENT,
                address_id INTEGER,
                FOREIGN KEY (
                    address_id
                )
                REFERENCES Addresses (address_id) ON UPDATE CASCADE
                                                ON DELETE CASCADE
            );


            -- Table: Groups
            DROP TABLE IF EXISTS [Groups];

            CREATE TABLE [Groups] (
                sevadar_id INTEGER,
                group_id   INTEGER,
                FOREIGN KEY (
                    group_id
                )
                REFERENCES GroupDetails (group_id) ON UPDATE CASCADE
                                                ON DELETE CASCADE,
                FOREIGN KEY (
                    sevadar_id
                )
                REFERENCES Sevadars (sevadar_id) ON UPDATE CASCADE
                                                ON DELETE CASCADE
            );


            -- Table: PoojaCount
            DROP TABLE IF EXISTS PoojaCount;

            CREATE TABLE PoojaCount (
                yyyymm TEXT    PRIMARY KEY,
                count  INTEGER
            );


            -- Table: SevadarAddress
            DROP TABLE IF EXISTS SevadarAddress;

            CREATE TABLE SevadarAddress (
                sevadar_id INTEGER,
                address_id INTEGER,
                FOREIGN KEY (
                    sevadar_id
                )
                REFERENCES Sevadars (sevadar_id) ON UPDATE CASCADE
                                                ON DELETE CASCADE,
                FOREIGN KEY (
                    address_id
                )
                REFERENCES Addresses (address_id) ON UPDATE CASCADE
                                                ON DELETE CASCADE
            );


            -- Table: Sevadars
            DROP TABLE IF EXISTS Sevadars;

            CREATE TABLE Sevadars (
                sevadar_id  INTEGER PRIMARY KEY AUTOINCREMENT,
                name        TEXT,
                rashi       INTEGER,
                nakshatra   INTEGER,
                gotra       INTEGER,
                pooja_basis INTEGER,
                pooja_date  INTEGER
            );


            -- Table: SevadarsFlexible
            DROP TABLE IF EXISTS SevadarsFlexible;

            CREATE TABLE SevadarsFlexible (
                sevadar_id INTEGER,
                FOREIGN KEY (
                    sevadar_id
                )
                REFERENCES Sevadars (sevadar_id) ON UPDATE CASCADE
                                                ON DELETE CASCADE
            );


            -- Table: SevaStartMonths
            DROP TABLE IF EXISTS SevaStartMonths;

            CREATE TABLE SevaStartMonths (
                sevadar_id   INTEGER,
                start_yyyymm TEXT,
                FOREIGN KEY (
                    sevadar_id
                )
                REFERENCES Sevadars (sevadar_id) ON UPDATE CASCADE
                                                ON DELETE CASCADE
            );


            -- View: SevadarDetails
            DROP VIEW IF EXISTS SevadarDetails;
            CREATE VIEW SevadarDetails AS
                SELECT s.*,
                    m.start_yyyymm,
                    IIF(f.sevadar_id = s.sevadar_id, TRUE, FALSE) AS flexible,
                    ga.group_id,
                    a.*
                FROM Sevadars s
                    LEFT JOIN
                    SevaStartMonths m ON s.sevadar_id = m.sevadar_id
                    LEFT JOIN
                    SevadarsFlexible f ON s.sevadar_id = f.sevadar_id
                    LEFT JOIN
                    SevadarAddress sa ON s.sevadar_id = sa.sevadar_id
                    LEFT JOIN
                    (
                        [Groups]
                        NATURAL JOIN
                        GroupDetails
                        NATURAL JOIN
                        Addresses
                    ) ga
                    ON ga.sevadar_id = s.sevadar_id
                    LEFT JOIN
                    Addresses a ON a.address_id = ga.address_id OR 
                                    a.address_id = sa.address_id;


            -- View: SevadarDetailsRecent
            DROP VIEW IF EXISTS SevadarDetailsRecent;
            CREATE VIEW SevadarDetailsRecent AS
                SELECT *
                FROM (
                        SELECT *
                            FROM SevadarDetails
                            ORDER BY start_yyyymm DESC
                    )
                GROUP BY sevadar_id;


            -- View: x
            DROP VIEW IF EXISTS x;
            CREATE VIEW x AS
                SELECT *,
                    start_yyyymm || '-00' AS end_yyyymm
                FROM SevaStartMonths;


            COMMIT TRANSACTION;
            PRAGMA foreign_keys = on;

        '''
    )
    conn.commit()
    # cur.execute(
    #     '''
    #         CREATE TABLE IF NOT EXISTS Sevadars(
    #             sevadar_id  INTEGER PRIMARY KEY AUTOINCREMENT,
    #             name        TEXT,
    #             rashi       INTEGER,
    #             nakshatra   INTEGER,
    #             gotra       INTEGER,
    #             pooja_basis INTEGER,
    #             pooja_date  INTEGER
    #         );
    #     '''
    # )
    # conn.commit()
    # cur.execute(
    #     '''
    #         CREATE TABLE IF NOT EXISTS Addresses(
    #             address_id  INTEGER PRIMARY KEY AUTOINCREMENT,
    #             line1       TEXT,
    #             line2       TEXT,
    #             line3       TEXT,
    #             line4       TEXT
    #         );
    #     '''
    # )
    # conn.commit()
    # cur.execute(
    #     '''
    #         CREATE TABLE IF NOT EXISTS GroupDetails(
    #             group_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    #             address_id  INTEGER,
    #             FOREIGN KEY(address_id)
    #                 REFERENCES Addresses(address_id)
    #                     ON UPDATE CASCADE
    #                     ON DELETE CASCADE
    #         );
    #     '''
    # )
    # conn.commit()
    # cur.execute(
    #     '''
    #         CREATE TABLE IF NOT EXISTS Groups(
    #             sevadar_id  INTEGER,
    #             group_id    INTEGER,
    #             FOREIGN KEY(group_id)
    #                 REFERENCES GroupDetails(group_id)
    #                     ON UPDATE CASCADE
    #                     ON DELETE CASCADE,
    #             FOREIGN KEY(sevadar_id)
    #                 REFERENCES Sevadars(sevadar_id)
    #                     ON UPDATE CASCADE
    #                     ON DELETE CASCADE
    #         );
    #     '''
    # )
    # conn.commit()
    # cur.execute(
    #     '''
    #         CREATE TABLE IF NOT EXISTS SevadarAddress(
    #             sevadar_id  INTEGER,
    #             address_id  INTEGER,
    #             FOREIGN KEY(sevadar_id)
    #                 REFERENCES Sevadars(sevadar_id)
    #                     ON UPDATE CASCADE
    #                     ON DELETE CASCADE,
    #             FOREIGN KEY(address_id)
    #                 REFERENCES Addresses(address_id)
    #                     ON UPDATE CASCADE
    #                     ON DELETE CASCADE
    #         );
    #     '''
    # )
    # conn.commit()
    # cur.execute(
    #     '''
    #         CREATE TABLE IF NOT EXISTS SevaStartMonths(
    #             sevadar_id INTEGER,
    #             start_yyyymm TEXT,
    #             FOREIGN KEY (sevadar_id)
    #                 REFERENCES Sevadars(sevadar_id)
    #                     ON UPDATE CASCADE
    #                     ON DELETE CASCADE
    #         );
    #     '''
    # )
    # conn.commit()
    # cur.execute(
    #     '''
    #         CREATE TABLE IF NOT EXISTS SevadarsFlexible(
    #             sevadar_id          INTEGER,
    #             FOREIGN KEY (sevadar_id)
    #                 REFERENCES Sevadars(sevadar_id)
    #                     ON UPDATE CASCADE
    #                     ON DELETE CASCADE
    #         );
    #     '''
    # )
    # conn.commit()
    # cur.execute(
    #     '''
    #         CREATE TABLE IF NOT EXISTS PoojaCount(
    #             yyyymm  TEXT PRIMARY KEY,
    #             count INTEGER
    #         );
    #     '''
    # )
    # conn.commit()
except Error as e:
    print('SQLite Error:',e)
finally:
    conn.close()



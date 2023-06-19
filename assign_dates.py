from thirdparty.panchanga import panchanga as pan
import pandas as pd
from calendar import monthcalendar, monthrange
import sqlite3
import traceback


def calc_decrement(n, limit): return n - 1 if n > 1 else limit
# print(calc_decrement(25,27))


def parse_weekday(day): return (day+5) % 7


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def calc_panchanga(year, month):
    a = pd.DataFrame(
        {'date': [i+1 for i in range(monthrange(year, month)[1])]})

    a['jd'] = a.apply(lambda row: pan.gregorian_to_jd(
        pan.Date(year, month, row.date)), axis=1)
    a['nakshatra'] = a.apply(lambda row: pan.nakshatra(
        row.jd, pan.mangaluru)[0], axis=1)
    a['tithi'] = a.apply(lambda row: pan.tithi(
        row.jd, pan.mangaluru)[0], axis=1)
    a['masa'] = a.apply(lambda row: pan.masa(row.jd, pan.mangaluru), axis=1)
    a['ritu'] = a.apply(lambda row: pan.ritu(row.masa[0]), axis=1)
    a['ayana'] = a.apply(lambda row: str(month)+str(row.jd)
                         < '0714' and str(month)+str(row.jd) > '0114', axis=1)
    a['samvatsara'] = a.apply(
        lambda row: pan.samvatsara(row.jd, row.masa[0]), axis=1)
    # print(a)
    return a


def assign_dates(database, year, month):
    month_panchanga = calc_panchanga(year, month)
    # print(
    #     int(month_panchanga[month_panchanga['nakshatra'] == 22].date.head(1)))
    month_calendar = monthcalendar(year, month)
    total_days = monthrange(year, month)[1]
    assigned_sevadars = {i+1: [] for i in range(monthrange(year, month)[1])}
    # print(assigned_sevadars)
    try:
        con = sqlite3.connect(database)
        con.row_factory = dict_factory
        cur = con.cursor()
        # cur.execute(f"""
        #     SELECT sevadar_id,pooja_basis, pooja_date,flexible
        #         FROM SevadarDetails
        #             NATURAL JOIN
        #             SevaStartMonths
        #         GROUP BY SevaStartMonths.sevadar_id
        #     HAVING MAX(SevaStartMonths.start_yyyymm) > '{year-1}-{month}';
        # """)
        # print(f"'{year-1}-{format(month,'02d')}'")
        cur.execute(f"""
            SELECT sevadar_id,pooja_basis, pooja_date,flexible
                FROM SevadarDetails
            where (start_yyyymm > '{year-1}-{format(month,'02d')}' AND start_yyyymm <= '{year}-{format(month,'02d')}');
        """)
        x = cur.fetchall()

        # print()
        # print("x", x)
        flexible = []

        ##################################################################################################################################
        ########################## Assign all non flexible sevadars ######################################################################
        ##################################################################################################################################

        for i in x:
            if i['flexible']:
                flexible.append(i)
                # print('flexible', i['sevadar_id'])
                continue
            sevadar_id = i['sevadar_id']
            basis = i['pooja_basis']
            date = i['pooja_date']
            d = 0
            # print('sid:',sevadar_id)
            if basis == 0:
                d = date if date <= total_days else total_days

            elif basis == 1:
                d = month_panchanga[month_panchanga['nakshatra'] == date].date.head(
                    1)
                while d.empty:
                    d = month_panchanga[month_panchanga['nakshatra']
                                        == calc_decrement(date, 27)].date.head(1)
            elif basis == 2:
                weekno = date//10
                day = parse_weekday(date % 10)
                week_index = 0
                for week in month_calendar:
                    if week[day] != 0:
                        week_index += 1
                        if week_index == weekno:
                            d = week[day]

                # if weekno > len(month_calendar)-1:
                #     weekno = len(month_calendar)-1
                # d = month_calendar[weekno][(day+5) % 7]
                # while d == 0:
                #     d = month_calendar[weekno-1][(day+5) % 7]
            elif basis == 3:
                d = month_panchanga[month_panchanga['tithi']
                                    == date].date.head(1)
                while d.empty:
                    d = month_panchanga[month_panchanga['tithi']
                                        == calc_decrement(date, 30)].date.head(1)

            assigned_sevadars[int(d)].append(sevadar_id)
            # print()
            # print(i)
            # print(assigned_sevadars)

        print("Non flexible")
        print(flexible)
        print(assigned_sevadars)

        ##################################################################################################################################
        ################################# Assign flexible sevadars if their prefered slot is available  ##################################
        ##################################################################################################################################

        flexible_ = flexible.copy()
        for i_ in range(len(flexible)):
            i = flexible[i_]
            sevadar_id = i['sevadar_id']
            basis = i['pooja_basis']
            date = i['pooja_date']
            # print('sid:', sevadar_id)
            if basis == 0:
                d = date if date <= total_days else total_days
            elif basis == 1:
                d = month_panchanga[month_panchanga['nakshatra'] == date].date.head(
                    1)
                if d.empty:
                    d = month_panchanga[month_panchanga['nakshatra']
                                        == calc_decrement(date, 27)].date.head(1)
            elif basis == 2:
                weekno = date//10
                day = parse_weekday(date % 10)
                week_index = 0
                for week in month_calendar:
                    if week[day] != 0:
                        week_index += 1
                        if week_index == weekno:
                            d = week[day]
                # weekno = date//10
                # day = date % 10
                # if weekno > len(month_calendar)-1:
                #     weekno = len(month_calendar)-1
                # d = month_calendar[weekno][(day-5) % 7]
                # while d == 0:
                #     d = month_calendar[weekno-1][(day-5) % 7]
            elif basis == 3:
                d = month_panchanga[month_panchanga['tithi']
                                    == date].date.head(1)
                if d.empty:
                    d = month_panchanga[month_panchanga['tithi']
                                        == calc_decrement(date, 30)].date.head(1)
            if len(assigned_sevadars[int(d)]) == 0:
                assigned_sevadars[int(d)].append(sevadar_id)
                flexible_.remove(i)
            else:
                flexible_.remove(i)
                i['d'] = int(d)
                flexible_.append(i)

        flexible = flexible_.copy()

        print("\nFlexible with their preference")
        print(flexible)
        print(assigned_sevadars)

        ##################################################################################################################################
        ################################# Fill empty slots with remaining flexible sevadars ##############################################
        ##################################################################################################################################

        date_iter = 1
        flexible_ = flexible.copy()
        for i_ in range(len(flexible)):
            i = flexible[i_]
            # print('sid:', i['sevadar_id'])

            while date_iter < total_days and assigned_sevadars[date_iter]:
                date_iter += 1
            assigned_sevadars[date_iter].append(i['sevadar_id'])
            flexible_.remove(i)
            # if not assigned_sevadars[date_iter]:
            # date_iter += 1
            # if date_iter > total_da
        flexible = flexible_
        print("\nFill Empty with flexible")
        print(flexible)
        print(assigned_sevadars)

        ##################################################################################################################################
        ################################# Assign remaining sevadars with preferred #######################################################
        ##################################################################################################################################

        for i in flexible:
            assigned_sevadars[i['d']].append(i['sevadar_id'])

        # print("\nFill with prefered")
        # print(flexible)
        print(assigned_sevadars)
        return assigned_sevadars
    except Exception as e:
        print(traceback.format_exc())
    finally:
        con.close()


if __name__ == '__main__':
    assign_dates('data/Seva_manager.db', 2023, 6)

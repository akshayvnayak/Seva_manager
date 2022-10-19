from thirdparty.panchanga import panchanga as pan
import pandas as pd
from calendar import monthcalendar, monthrange
import sqlite3
import traceback
from random import randint

calc_decrement = lambda n,limit: n - 1 if n>1 else limit
# print(calc_decrement(25,27))

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def calc_panchanga(year,month):
    a = pd.DataFrame({'date':[i+1 for i in range(monthrange(year,month)[1])]})

    a['jd'] =a.apply( lambda row: pan.gregorian_to_jd(pan.Date(year,month,row.date)),axis = 1)
    a['nakshatra'] =a.apply(lambda row: pan.nakshatra(row.jd,pan.mangaluru)[0],axis = 1)
    a['tithi'] = a.apply(lambda row: pan.tithi(row.jd,pan.mangaluru)[0],axis = 1)
    a['masa'] = a.apply(lambda row: pan.masa(row.jd, pan.mangaluru),axis = 1)
    a['ritu'] = a.apply(lambda row: pan.ritu(row.masa[0]),axis = 1)
    a['ayana'] = a.apply(lambda row: str(month)+str(row.jd) < '0714' and str(month)+str(row.jd) > '0114',axis=1)
    a['samvatsara'] = a.apply(lambda row: pan.samvatsara(row.jd,row.masa[0]),axis = 1)
    # print(a)
    return a

def assign_dates(database,year,month):
    month_panchanga = calc_panchanga(year,month)
    print(int(month_panchanga[month_panchanga['nakshatra'] == 22].date.head(1)))
    month_calendar = monthcalendar(year,month)
    assigned_sevadars = {i+1:[] for i in range(monthrange(year,month)[1])}
    print(assigned_sevadars)
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

        print()
        print("x",x)
        flexible = []


        ##################################################################################################################################
        ########################## Assign all non flexible sevadars ######################################################################
        ##################################################################################################################################

        for i in x:
            if i['flexible']:
                flexible.append(i)
                continue
            sevadar_id = i['sevadar_id']
            basis = i['pooja_basis']
            date = i['pooja_date']
            # print('sid:',sevadar_id)
            if basis == 0:
                d = date
            elif basis == 1:
                d = month_panchanga[month_panchanga['nakshatra'] == date].date.head(1)
                if d.empty:
                    d = month_panchanga[month_panchanga['nakshatra'] == calc_decrement(date,27)].date.head(1)
            elif basis == 2:
                weekno = date//10
                day = date%10
                if weekno>len(month_calendar)-1: weekno = len(month_calendar)-1
                d = month_calendar[weekno][day]
                while d ==0: d = month_calendar[weekno-1][day]
            elif basis == 3:
                d = month_panchanga[month_panchanga['tithi'] == date].date.head(1)
                if d.empty:
                    d = month_panchanga[month_panchanga['tithi'] == calc_decrement(date,30)].date.head(1)

            assigned_sevadars[int(d)].append(sevadar_id)
            print()
            print(i)
            print(assigned_sevadars)
        
        print(flexible)
        # print(assigned_sevadars)


        ##################################################################################################################################
        ################################# Assign flexible sevadars if their prefered slot is available  ##################################
        ##################################################################################################################################
        
        flexible_ = flexible
        for i in flexible:
            sevadar_id = i['sevadar_id']
            basis = i['pooja_basis']
            date = i['pooja_date']
            # print('sid:',sevadar_id)
            if basis == 0:
                d = date
            elif basis == 1:
                d = month_panchanga[month_panchanga['nakshatra'] == date].date.head(1)
                if d.empty:
                    d = month_panchanga[month_panchanga['nakshatra'] == calc_decrement(date,27)].date.head(1)
            elif basis == 2:
                weekno = date//10
                day = date%10
                if weekno>len(month_calendar)-1: weekno = len(month_calendar)-1
                d = month_calendar[weekno][day]
                while d ==0: d = month_calendar[weekno-1][day]
            elif basis == 3:
                d = month_panchanga[month_panchanga['tithi'] == date].date.head(1)
                if d.empty:
                    d = month_panchanga[month_panchanga['tithi'] == calc_decrement(date,30)].date.head(1)
            if not assigned_sevadars[int(d)]:
                assigned_sevadars[int(d)].append(sevadar_id)
                flexible_.remove(i)
        flexible = flexible_

        # print(flexible)


        ##################################################################################################################################
        ################################# Fill empty slots with remaining flexible sevadars ##############################################
        ##################################################################################################################################

        date_iter = 1
        total_days = monthrange(year,month)[1]
        for i in flexible:
            if not assigned_sevadars[date_iter]:
                assigned_sevadars[date_iter].append(i['sevadar_id'])
                flexible_.remove(i)
            date_iter +=1
            if date_iter > total_days:
                date_iter = 1
        flexible = flexible_
        # print(flexible)


        ##################################################################################################################################
        ################################# Assign remaining sevadars with random dates  ###################################################
        ##################################################################################################################################

        for i in flexible:
            assigned_sevadars[randint(1,total_days)].append(i['sevadar_id'])

        print(assigned_sevadars)
        return assigned_sevadars
    except Exception as e:
        print(traceback.format_exc())
    finally:
        con.close()

if __name__ == '__main__':
    assign_dates('data/Seva_manager.db',2022,11)
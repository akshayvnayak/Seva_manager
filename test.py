from thirdparty.panchanga import panchanga
import swisseph as swe
import datetime
import pandas as pd
# print(panchanga.gregorian_to_jd( datetime.date.today()))
import sqlite3
import SanskritNames as sdict

m = panchanga.Place(12.91723,74.85603,+5.5)
# date = panchanga.gregorian_to_jd(panchanga.Date(2021,7,19))
# while date != panchanga.gregorian_to_jd(datetime.date.today()):
#     print(panchanga.jd_to_gregorian(date),panchanga.tithi(date,m),panchanga.masa(date,m),panchanga.samvatsara(date,panchanga.masa(date,m)[0]),panchanga.nakshatra(date,m))
#     date+=1

# from calendar import calendar, monthrange
# import calendar

# print(calendar.month_name())

con = sqlite3.connect("data/Seva_manager.db")

# Load the data into a DataFrame
surveys_df = pd.read_sql_query("SELECT * from sevadardetails", con)
print(surveys_df[surveys_df.start_yyyymm > '2021-02'].start_yyyymm)
con.close()

con = sqlite3.connect("data.panchanga_trial.db")

date = panchanga.gregorian_to_jd(panchanga.Date(2020,8,19))

def normaldate(jd):
    a = panchanga.jd_to_gregorian(jd)
    return str(a[0])+'-'+str(a[1])+'-'+str(a[2])

tithi = lambda jd: [sdict.tithis[str(t[0])] for t in panchanga.tithi(jd,panchanga.mangaluru)]

masa = lambda jd: sdict.masas(str(panchanga.masa(jd,panchanga.mangaluru)[0]))

samvatsara = lambda jd


while date != panchanga.gregorian_to_jd(datetime.date.today()):
    tithi = 
    print(panchanga.jd_to_gregorian(date),panchanga.tithi(date,m),panchanga.masa(date,m),panchanga.samvatsara(date,panchanga.masa(date,m)[0]),panchanga.nakshatra(date,m))

    date+=1
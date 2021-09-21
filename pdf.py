from calendar import calendar
from datetime import datetime
import sqlite3
from traceback import format_exc
from assign_dates import assign_dates

from fpdf import FPDF
from SanskritNames import samvatsaras,gotras
from thirdparty.panchanga import panchanga as pan

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def create_pdf(year,month):
    calendar_dict = assign_dates('data/Seva_manager.db',year,month)
    seva_order = []
    total_count = 0
    for i in calendar_dict:
        total_count+=len(calendar_dict[i])
    # print(total_count)
    try:
        conn = sqlite3.connect('data\Seva_manager.db')
        conn.row_factory = dict_factory
        cur = conn.cursor()
        # print("Opened database successfully")

        ######## Create a dictionary seva_order, with pno as key and sevadar_details as value

        prev_month = str(year if month > 1 else year-1) + '-' + format(month-1 if month > 1 else 12, '02d')
        cur.execute(f"select count from PoojaCount where yyyymm = '{prev_month}'")
        pno = cur.fetchone()
        if not pno: 
            pno = total_count+1
        else:
            pno = pno['count'] + total_count+1
            
        # pno = 20

        group = {}
        group_env = []
        for i in reversed(calendar_dict):
            for s_id in calendar_dict[i]:
                cur.execute(f"""
                        select 
                            sevadar_id, name, rashi, nakshatra, gotra, start_yyyymm,
                            group_id, line1, line2, line3, line4
                        from SevadarDetailsRecent where sevadar_id = {s_id}
                        
                        """)
                pno-=1
                # print(s_id,pno)
                # seva_order[pno] = cur.fetchone()
                sevadar_details = cur.fetchone()
                # print(pno,seva_order[pno])
                # print()
                if (g:=sevadar_details['group_id']) != None:
                    # print(sevadar_details)
                    if g not in group:
                        group[g] = {'pno':pno,'group_date': i}
                        group_env.append(sevadar_details['sevadar_id'])
                    sevadar_details['pno'] = str(group[g]['pno'])+'/'+str(group[g]['group_date'])
                else:
                    sevadar_details['pno'] = str(pno)
                sevadar_details['date'] = i
                # print(sevadar_details,sevadar_details['line1'])
                seva_order.append(sevadar_details)

        # print(pno)
        cur.execute(f"insert or replace into PoojaCount values('{str(year)+'-'+format(month,'02d')}',{pno+total_count-1})")
        conn.commit()

    except Exception as e:
            print(format_exc())
    finally:
        conn.close()


    ####################################################################################################
    ########################################### Create a pdf ###########################################
    ####################################################################################################

    pdf = FPDF('L','mm',(99,210))
    env_pdf = FPDF('L','mm',(109.5502 , 219.075))
    # env_pdf.compress = False
    env_pdf.set_font('Arial', '', 12)
    pdf.compress = False

    first_day = datetime(year,month,1).weekday()

    for i in reversed(seva_order):
        name = i['name']
        date = format(i['date'],'02d')+'-'+format(month,'02d')+'-'+str(year)
        pno = str(i['pno'])
        pcount = format((month - int(i['start_yyyymm'][-2:])+13)%12,'02d')

        d = pan.gregorian_to_jd(pan.Date(year,month,i['date']))
        vaara = (first_day+i['date'])%6 + 1
        tithi = pan.tithi(d,pan.mangaluru)[0]
        if tithi > 15:
            paksha = 2
            tithi = tithi-15
        else:
            paksha = 1
        maasa = pan.masa(d,pan.mangaluru)[0]
        ritu = (maasa+1)//2
        comp_date = format(month,'02d')+format(i['date'],'02d')
        ayana = int(comp_date >= '0114' and comp_date <= '0714')+1
        samvatsara = pan.samvatsara(d,maasa)

        rashi = i['rashi']
        nakshatra = i['nakshatra']
        gotra = i['gotra']
        # print(i['line1'])
        # print(group)
        if i['group_id'] == None or (i['sevadar_id'] in group_env):
            # l1 = str(i['pno'])
            # print(l1)
            env_pdf.add_page()
            env_pdf.image('template_preperation/envelope_without_address.jpg',0,0,219.075,109.5502)
            env_pdf.text(20,48,pno)
            env_pdf.text(110,48,i['line1'])
            env_pdf.text(110,56.15,i['line2'])
            env_pdf.text(110,64.3,i['line3'])
            env_pdf.text(110,72.45,i['line4'])


        pdf.add_page()
        pdf.image("template_preperation/invoice.jpg", 0, 0,210,99)

        pdf.set_font('Arial', 'B', 13.5)
        pdf.text(58,39.5,name)
        pdf.text(128,48.2,pcount)

        pdf.set_font('Arial', '', 13)
        pdf.text(29,28,pno)
        pdf.text(163,28,date)

        pdf.image(f"template_preperation/samvatsaras/{samvatsara}.jpg", 10, 52.3,h = 7)
        pdf.image(f"template_preperation/ayanas/{ayana}.jpg", 63, 52.15,h = 7)
        pdf.image(f"template_preperation/ritus/{ritu}.jpg", 99, 52.2,h = 7)
        pdf.image(f"template_preperation/maasas/{maasa}.jpg", 133.5, 52.3,h = 7)
        pdf.image(f"template_preperation/pakshas/{paksha}.jpg", 170.5, 52.2,h = 7)

        pdf.image(f"template_preperation/tithis/{tithi}.jpg", 14, 61.27,h = 7)
        pdf.image(f"template_preperation/vaaras/{vaara}.jpg", 50, 61,h = 7)

        pdf.image(f"template_preperation/rashis/{rashi}.jpg", 26, 83,h = 7)
        pdf.image(f"template_preperation/nakshatras/{nakshatra}.jpg", 78.5, 83,h = 7)
        pdf.text(159,87.6,gotras[f'{gotra}'])

    pdf.output('out.pdf', 'F')
    env_pdf.output('env.pdf','F')


if __name__ == "__main__":
    create_pdf(2021,1)
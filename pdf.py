import sqlite3
from traceback import format_exc
from assign_dates import assign_dates

from fpdf import FPDF
from SanskritNames import samvatsaras

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def create_pdf(year,month):
    calendar_dict = assign_dates('data/Seva_manager.db',year,month)
    seva_order = []
    try:
        conn = sqlite3.connect('data\Seva_manager.db')
        conn.row_factory = dict_factory
        cur = conn.cursor()
        print("Opened database successfully")

        ######## Create a dictionary seva_order, with pno as key and sevadar_details as value

        prev_month = str(year if month > 1 else year-1) + '-' + format(month-1 if month > 1 else 12, '02d')
        cur.execute(f"select count from PoojaCount where yyyymm = '{prev_month}'")
        pno = cur.fetchone()
        if not pno: 
            pno = 0
        else:
            pno = pno['count'] 
            
        # pno = 20

        group = {}
        for i in reversed(calendar_dict):
            for s_id in calendar_dict[i]:
                cur.execute(f"""
                        select 
                            sevadar_id, name, rashi, nakshatra, gotra, start_yyyymm,
                            group_id, line1, line2, line3, line4
                        from SevadarDetailsRecent where sevadar_id = {s_id}
                        
                        """)
                pno+=1
                # seva_order[pno] = cur.fetchone()
                sevadar_details = cur.fetchone()
                # print(pno,seva_order[pno])
                # print()
                if g:=sevadar_details['group_id'] != None:
                    # print(sevadar_details)
                    if g not in group:
                        group[g] = {'pno':pno,'group_date': i}
                    sevadar_details['pno'] = str(group[g]['pno'])+'/'+str(group[g]['group_date'])
                else:
                    sevadar_details['pno'] = str(pno)
                sevadar_details['date'] = i
                print(sevadar_details)
                seva_order.append(sevadar_details)


        cur.execute(f"insert or replace into PoojaCount values('{str(year)+'-'+format(month,'02d')}',{pno})")
        conn.commit()

    except Exception as e:
            print(format_exc())
    finally:
        conn.close()

    ################### Create a pdf #################################



    pdf = FPDF('L','mm',(99,210))    
    pdf.compress = False

    for i in reversed(seva_order):
        name = i['name']
        date = format(i['date'],'02d')+'-'+format(month,'02d')+'-'+str(year)
        pno = str(i['pno'])
        pcount = format((month - int(i['start_yyyymm'][-2:])+13)%12,'02d')


        # samvatsara 

        gotra = 'Kashyapa'

        pdf.add_page()
        pdf.image("template_preperation/invoice.jpg", 0, 0,210,99)

        pdf.set_font('Arial', 'B', 13.5)
        pdf.text(58,39.5,name)
        pdf.text(128,48.2,pcount)

        pdf.set_font('Arial', '', 13)
        pdf.text(29,28,pno)
        pdf.text(163,28,date)

        i = 1
        pdf.image(f"template_preperation/samvatsaras/{samvatsara}.jpg", 10, 52.3,h = 7)
        pdf.image(f"template_preperation/ayanas/{i+1}.jpg", 63, 52.15,h = 7)
        pdf.image(f"template_preperation/ritus/{i+1}.jpg", 99, 52.2,h = 7)
        pdf.image(f"template_preperation/maasas/{i+1}.jpg", 133.5, 52.3,h = 7)
        pdf.image(f"template_preperation/pakshas/{i+1}.jpg", 170.5, 52.2,h = 7)

        pdf.image(f"template_preperation/tithis/{i+1}.jpg", 14, 61.27,h = 7)
        pdf.image(f"template_preperation/vaaras/{i+1}.jpg", 50, 61,h = 7)

        pdf.image(f"template_preperation/rashis/{i+1}.jpg", 26, 83,h = 7)
        pdf.image(f"template_preperation/nakshatras/{i+1}.jpg", 78.5, 83,h = 7)
        pdf.text(159,87.6,gotra)

    pdf.output('out.pdf', 'F')


if __name__ == "__main__":
    create_pdf(2021,1)
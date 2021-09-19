
from fpdf import FPDF

pdf = FPDF('P','mm',(210,99))
# compression is not yet supported in py3k version
pdf.compress = False
# Unicode is not yet supported in the py3k version; use windows-1252 standard font

for i in range(2):
    name = "Akshay V Nayak"
    date = '14-09-2000'
    pno = '1026'
    pcount = '05'
    gotra = 'Kashyapa'

    pdf.add_page()
    pdf.image("template_preperation/invoice.jpg", 0, 0,210,99)

    pdf.set_font('Arial', 'B', 13.5)
    pdf.text(58,39.5,name)
    pdf.text(128,48.2,pcount)

    pdf.set_font('Arial', '', 13)
    pdf.text(29,28,pno)
    pdf.text(163,28,date)


    pdf.image(f"template_preperation/samvatsaras/{i+1}.jpg", 10, 52.3,h = 7)
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
# -*- coding: UTF-8 -*-
# # from panchanga import panchanga
# # mangaluru = panchanga.Place(12.91723,74.85603,+5.5)
# # def tithi(dd,mm,yyyy):
# #     date = panchanga.gregorian_to_jd(panchanga.Date(yyyy,mm,dd))
# #     return panchanga.tithi(date,mangaluru)

# print(tithi(14,9,2000))


# Python program to create
# a pdf file

from __future__ import print_function
from fpdf import FPDF


print("ಸೀತಾರಾಮಾಂಜನೇ".encode(encoding="ascii",errors="xmlcharrefreplace"))
# save FPDF() class into a
# variable pdf
pdf = FPDF()

# Add a page
pdf.add_page()

# set style and size of font
# # that you want in the pdf
pdf.add_font("BRHKan01","",'./fonts/BRHKan01.ttf',uni=True)
pdf.set_font("BRHKan01", size = 15)

pdf.add_font('gargi', '', './fonts/gargi.ttf', uni=True) 
pdf.set_font('gargi', '', 14)
# pdf.write(8,u'PÉÆmÉ ²æÃ ¹ÃvÁgÁªÀiÁAd£ÉÃ')
# pdf.write(8, ('Hindi: नमस्ते दुनिया ಕೊಟೆ ಶ್ರೀ ಸೀತಾರಾಮಾಂಜನೇ'.encode(encoding="ascii",errors="xmlcharrefreplace")))
# create a cell
pdf.cell(200, 10, txt = 'Hindi: नमस्ते दुनिया ಕೊಟೆ ಶ್ರೀ ಸೀತಾರಾಮಾಂಜನೇ'.encode(encoding="ascii",errors="xmlcharrefreplace"),ln = 1, align = 'C')

# # add another cell
# pdf.cell(200, 10, txt = u"A C ಕೊಟೆ ಶ್ರೀ ಸೀತಾರಾಮಾಂಜನೇಯ geeks.",
# 		ln = 2, align = 'C')

# save the pdf with name .pdf
pdf.output("GFG.pdf")


# import speech_recognition as sr
# recognizer = sr.Recognizer()
# with sr.Microphone() as inputs:
#     print("Please speak now")
#     listening = recognizer.listen(inputs)
#     print("Analysing...")
#     try:
#         print("Did you say: "+recognizer.recognize_google(listening,language = "kn-IN"))
#         ent = (recognizer.recognize_google(listening,language = "kn-IN"))
#     except:
#          print("please speak again")

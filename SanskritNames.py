import json
with open("data/panchanga.json", encoding='utf8') as fp:
    sktnames = json.load(fp)
tithis = sktnames["tithis"]
nakshatras = sktnames["nakshatras"]
vaaras = sktnames["vaaras"]
masas = sktnames["maasas"]
samvatsaras = sktnames["samvatsaras"]
ritus = sktnames["ritus"]
rashis = sktnames["rashis"]
gotras = sktnames["gotras"]
months = {	'01':'Janauary',
		'02':'February',
		'03':'March',
		'04':'April',
		'05':'May',
		'06':'June',
		'07':'July',
		'08':'August',
		'09':'September',
		'10':'October',
		'11':'November',
		'12':'December'		}
pooja_basis = {	0:'Date',
				1:'Nakshatra',
				2:'Week no. & Day',
				3:'Tithi'}
# print(rashis)
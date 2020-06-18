import requests
import string 
import re 



struct = requests.get('http://dataservices.imf.org/REST/SDMX_JSON.svc/Dataflow')

#annual GDP values
def getTimeSeriesGDP(cc):
	GDPInd = 'NGDP_USD'
	cdata = requests.get('http://dataservices.imf.org/REST/SDMX_JSON.svc/CompactData/SNA/A.' + cc + '.' + GDPInd)
	return cdata.json()['CompactData']['DataSet']['Series']

def getCCodes(dbID):
	country_codes = []
	cc = re.compile('^[A-Z]{2}$')
	dbstruct = requests.get('http://dataservices.imf.org/REST/SDMX_JSON.svc/DataStructure/' + dbID)
	jsonlist = dbstruct.json()['Structure']['CodeLists']['CodeList'][2]['Code']
	for key in jsonlist:
		if cc.match(key['@value']):
			country_codes.append([key['@value'], key['Description']['#text']])
	return country_codes

def getWEODBCodes():
	ids = []
	df = struct.json()['Structure']['Dataflows']['Dataflow']
	for key in df:
		if 'Economic Outlook' in key['Name']['#text']:
			ids.append(key['@id'].rstrip(string.digits)[3:])
	ids.remove('APDREO2017M')
	return list(set(ids))

#for world economic outlook 
ccodes = []
dbcodes = ['SNA']
for i in dbcodes:
	ccodes.append(getCCodes(i))

for i in ccodes[0]:
	print('GDP values for ' + i[1])
	print(getTimeSeriesGDP(i[0]))

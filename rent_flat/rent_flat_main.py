import requests as r
import sys
from bs4 import BeautifulSoup
import datetime
from mongo import database

def dist_matrix(origin, dest):
	url = 'https://maps.googleapis.com/maps/api/distancematrix/json?'
	API_key = ''
	#destination = [] возможно узнать путь до несскольких пунктов
	if type(dest) is list: dest = ' | '.join(dest)
	payload = {
		'origins': origin,
		'destinations': dest,
		'mode': 'driving',
		'key': API_key
	}
	resp = r.get(url, params = payload)
	dist = []
	if resp.status_code == 200 and resp.json()['status'] == 'OK':
		for i in range(len(resp.json()['rows'][0]['elements'])):
			if resp.json()['rows'][0]['elements'][i]['status'] != 'NOT_FOUND':
				#km = resp.json()['rows'][0]['elements'][i]['distance']['text']
				km = (resp.json()['rows'][0]['elements'][i]['distance']['value'])/1000
				km = round(km,2)
				dist.append(km)
			else: dist.append(0)
	else: 
		print('Error API: ',resp.status_code, resp.json()['status'])	
	return dist


def parse():
	url = 'https://kaliningrad.irr.ru/real-estate/rent/'#сделать индексацию страниц
	res = r.get(url)
	if res.status_code == 200:
		res = BeautifulSoup(res.text, 'lxml')
		pages = int(res.findAll('a',{'class':'pagination__pagesLink'})[-1].text)
		#pages = 8
		res = []
	else: print('Error: 0th page')

	for p in range(1, pages+1):
		soup = r.get(url+'page'+str(p)+'/')
		if soup.status_code == 200:
			print('{0:d}th page'.format(p))
			soup = BeautifulSoup(soup.text, 'lxml')
			ads = soup.findAll('div',{'class':'listing__itemInner'})
			tmp = []

			for a in ads:
				try:
					addr = a.findAll('div',{'class':'listing__itemParameter listing__itemParameter_subTitleBold js-listingText'})[0].text
					if len(addr)>8:
						addr = 'Россия, Калининград, ' + addr
						price = a.findAll('div',{'class':'listing__itemPrice'})[0].text.replace(' ','').replace('\n','').replace('\t','').replace('\xa0','')[:-4]
						if price.isalnum():
							price = int(price)
						else: price = -1
						rooms = a.findAll('div',{'class':'js-productListingProductName'})[0].text
						floor = a.findAll('div',{'class':'listing__itemParameter js-cropRentParams'})[0].text
						tmp.append([addr, price, rooms, floor])
				except IndexError:
					pass

			dist = dist_matrix('Россия, Калининград, Невского, 14б', [i[0] for i in tmp])
			#dist = []
			if len(dist)==0: res = res + tmp
			else:
				for i in range(len(tmp)): 
					tmp[i].append(dist[i])
				res = res + tmp

		else: print('Error: {0:d}th page'.format(p))
	return res

def log(content):
	max_addr = max([len(i[0]) for i in content])
	name = datetime.datetime.now()
	f = open('/home/drem/log'+name.isoformat()[:-10], 'w')
	for row in content:
		f.write(row[0]+(max_addr-len(row[0]))*' ') #адрес
		f.write(row[3]+(15-len(row[3]))*' ') #этаж
		f.write(row[2]+(15-len(row[2]))*' ') #количество комнат
		f.write(str(row[1])+' руб'+(7-len(str(row[1])))*' ') #цена
		if len(row)==5: f.write(str(row[4])+' км') #расстояние
		f.write('\n')
	f.close()

def Create_db(data):
	db_name = 'rent_flat_db'
	col_name = 'site_ads'
	db_obj = database({'name':db_name})
	if col_name not in db_obj.db.collection_names():
		db_obj.db.create_collection('site_ads')	
		print('Collection \"{0:s}\" created'.format(col_name))
	'''	
	else:
		db_obj.db.drop_collection(col_name)
		db_obj.db.create_collection('site_ads')	
		print('Collection \"{0:s}\" created'.format(col_name))
	'''	

	for doc in data:
		if db_obj.db.col_name.find({'addr':doc[0]}).count()==0:
			db_obj.db.col_name.insert({'addr':doc[0], 'price':doc[1], 'rooms':doc[2], 'floor':doc[3]}) #? save()
		if len(doc)==5:
				db_obj.db.col_name.update({'addr':doc[0]},{'$set':{'dist_km': doc[4]}})

	print(db_obj.db.col_name.count())
	print(db_obj.db.col_name.find({'dist_km': {'$exists':True}}).count())

	'''
	for i in db_obj.db.col_name.find():
		print(i)
	'''	

def main():
	#Create_db([['Россия, Калининград, Горького ул, 172',12000 ,'2-комн. кв.','эт. 5 / 9', '5.9 km'] ,['Россия, Калининград, Житомерская, 10-14',9000 ,'1-комн. кв.', 'эт. 2 / 4','3.6 km']])
	data = parse()
	log(data)
	Create_db(data)

if __name__ == '__main__':
	main()

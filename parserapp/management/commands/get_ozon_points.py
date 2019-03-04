from django.core.management.base import BaseCommand
#from ...models import Points, Gallery, Coordinates, Structured_address
#from django.core.files.storage import default_storage
from django.conf import settings
#from parserapp.client import make_api_request
from json.decoder import JSONDecodeError
from parserapp.models import OzonPoints, AreaList
import requests
import json

import unicodedata

def update_points(data):
	#OzonPoints.objects.all().delete()
	for i in data:

		point, create = OzonPoints.objects.get_or_create(idd=i.get('id'),
		                                 defaults={
			                                 "name": i.get('name')[:250],
			                                 "address": i.get('address')[:250]
		                                 })
		if create:
			try:
				point.metro = i.get('metro')[:250]
				point.save()
			except:
				print('Error create metro')
				

def get_ozon_points(areaId):
	url = 'https://www.ozon.ru/json/pvzservice.asmx/getbyareaid'
	requests_method = getattr(requests, 'post')
	headers = {'Content-Type': 'application/json',
	           'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) '
	                         'Chrome/39.0.2171.95 Safari/537.36'}
	request = requests_method(url, headers=headers, json={"areaId": areaId})
	if request.status_code in (200, 201):
		try:
			return json.loads(request.json().get('d', None).get('data'))
		except Exception as e:
			return 'Error get data, exception: {}'.format(e)
	return 'no data, response text: {}'.format(request.text)
	
	
	
def get_data(areaId=2, token='cWwN7QB86Ei9ExsJD8cx'):
	url = 'https://api.ozon.ru/checkout/v7/checkout'
	url2 = 'https://www.ozon.ru/json/pvzservice.asmx/getbyareaid'
	requests_method = getattr(requests, 'post')
	headers = {'authorization': 'Bearer {}'.format(token),  # 'Origin': 'https://www.ozon.ru',
		'Content-Type': 'application/json',
		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) '
		              'Chrome/39.0.2171.95 Safari/537.36'}
	# 'x-o3-app-handler':'Checkout/Checkout',
	# 'x-o3-app-name': 'ozon_new',
	# 'X-OZON-ABGROUP': '44'}
	request2 = {"areaId": areaId}
	get_request = requests_method(url2, headers=headers, json=request2)
	if get_request.status_code in (200, 201):
		message = get_request.json()
		flag = True
		try:
			data = json.loads(message.get('d', None).get('data'))
			print(data)#, message)
			#data = message.get('data')['delivery']['deliveryTypes'][0]
		except:
			flag = False
			print('no data')
			
		if flag:
			update_points(data)
		# try:
		# 	message = get_request.json()
		# 	#print(message.get('data')['delivery']['deliveryTypes'][0]['deliveryMethods'])
		# 	save_data(message.get('data')['delivery']['deliveryTypes'][0]['deliveryMethods'])
		# except JSONDecodeError:
		# 	print(get_request.text)
		# 	return get_request.text
		# except:
		# 	print(message.get('data')['delivery']['deliveryTypes'])
		# 	return get_request.text  # return get_request.text
	else:
		return get_request.text
	
	#session = requests.Session()
	#headers[
	#	'cookie'] = 'incap_ses_379_1101384=vFcsclCzMGKRbKeXiXpCBYTkc1wAAAAA1+mPaDvE2Kj0GTHKm51zyQ==; visid_incap_1101384=TymqMYLcRIu019kVCbOcPYTkc1wAAAAAQUIPAAAAAAA9yQgs02stgP4xQH+R1CCl'
	
	#response = session.get(url='https://www.ozon.ru/checkout', headers=headers)
	#print(response.cookies.get_dict())


# response = response.get(url='https://www.ozon.ru/checkout')
# print(response.cookies.get_dict())

class Command(BaseCommand):
	help = 'Generates Fake data'
	
	def handle(self, *args, **options):
		token = 'cWwN7QB86Ei9ExsJD8cx'
		# area_list = AreaList.objects.all()
		# for area in area_list:
		# 	get_data(area.idd, token)

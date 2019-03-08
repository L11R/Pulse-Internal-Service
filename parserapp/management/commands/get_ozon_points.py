from django.core.management.base import BaseCommand
# from ...models import Points, Gallery, Coordinates, Structured_address
# from django.core.files.storage import default_storage
from django.conf import settings
# from parserapp.client import make_api_request
from json.decoder import JSONDecodeError
from parserapp.models import OzonPoints, AreaList
import requests
import json

import unicodedata


def update_points(data):
	# OzonPoints.objects.all().delete()
	for i in data:
		
		point, create = OzonPoints.objects.get_or_create(idd=i.get('id'), defaults={"name": i.get('name')[:250],
			"address": i.get('address')[:250]})
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


def get_bringly_points():
	url = "https://bringly.ru/api/resolve/?r=checkout:resolveGetPickupPoints"
	payload = {"params": [{
		"outletsIds": [67121184, 67121185, 67121186, 67121187, 67121188, 67121189, 67121190, 67121191, 67121192,
		               67121193, 67121194, 67121195, 67121196, 67121197, 67121198, 67121199, 67121200, 67121201,
		               67121202, 63286860], "_isRemoteCall": True}],
		"path": "/checkout/8fa6d294-4b5a-41b1-a695-ae71695e4c3e"}
	requests_method = getattr(requests, 'post')
	headers = {'Content-Type': 'application/json',
	           'sk': 'u9883e91690bdfd14930bde52f5ed0369',
	           'Referer': "https://bringly.ru/checkout/8fa6d294-4b5a-41b1-a695-ae71695e4c3e",
	           'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) '
	                         'Chrome/39.0.2171.95 Safari/537.36'}
	COOKIES = {
	           "Session_id": "3:1551954404.5.4.1527268153432:otiGBQ:43.1|601485522.0.2|566404027.27.2.2:27|512709374.14694287.2.2:14694287|1130000031398501.14694371.2.2:14694371|1130000033447162.20160640.2.2:20160640|47:4360.900314.lv_OTl8CGBMeb5iYx2sA0b4PWRE"
	}
	url2 = "https://bringly.ru/api/resolve/?r=checkout:resolveGetPickupPoints"
	payload2 = {"params":[{"outletsIds":[68410451,68410452,68410454,68410455,68410456,68410457,67384590,67384591,67121172,67121173,67121174,67121175,67121176,67121177,67121178,67121179,67121180,67121181,67121182,67121183],"_isRemoteCall":True}],"path":"/checkout/8fa6d294-4b5a-41b1-a695-ae71695e4c3e"}
	request = requests_method(url, headers=headers, data=json.dumps(payload), cookies=COOKIES)
	request2 = requests_method(url2, headers=headers, data=json.dumps(payload2), cookies=COOKIES)
	if request.status_code in (200, 201):
		try:
			return request.json(), request2.json()
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
			print(data)  # , message)  # data = message.get('data')['delivery']['deliveryTypes'][0]
		except:
			flag = False
			print('no data')
		
		if flag:
			update_points(
				data)  # try:  # 	message = get_request.json()  # 	#print(message.get('data')['delivery']['deliveryTypes'][0]['deliveryMethods'])  # 	save_data(message.get('data')['delivery']['deliveryTypes'][0]['deliveryMethods'])  # except JSONDecodeError:  # 	print(get_request.text)  # 	return get_request.text  # except:  # 	print(message.get('data')['delivery']['deliveryTypes'])  # 	return get_request.text  # return get_request.text
	else:
		return get_request.text


# session = requests.Session()
# headers[
#	'cookie'] = 'incap_ses_379_1101384=vFcsclCzMGKRbKeXiXpCBYTkc1wAAAAA1+mPaDvE2Kj0GTHKm51zyQ==; visid_incap_1101384=TymqMYLcRIu019kVCbOcPYTkc1wAAAAAQUIPAAAAAAA9yQgs02stgP4xQH+R1CCl'

# response = session.get(url='https://www.ozon.ru/checkout', headers=headers)
# print(response.cookies.get_dict())


# response = response.get(url='https://www.ozon.ru/checkout')
# print(response.cookies.get_dict())

class Command(BaseCommand):
	help = 'Generates Fake data'
	
	def handle(self, *args, **options):
		data, data2 = get_bringly_points()
		print(data, '\n\n', data2)
		#token = 'cWwN7QB86Ei9ExsJD8cx'  # area_list = AreaList.objects.all()  # for area in area_list:  # 	get_data(area.idd, token)
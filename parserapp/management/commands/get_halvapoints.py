from django.core.management.base import BaseCommand
import requests
import json
from parserapp.models import HalvaPoint
from django.conf import settings


def send_request(token, url, payload):
	HDRS = {'Content-type': 'application/json', 'Encoding': 'utf-8'}
	headers = HDRS.copy()
	headers['Authorization'] = token
	response = requests.get(url, verify=False, data=json.dumps(payload), headers=headers)
	return response


def update_or_create_halva_points(points):
	for point in points:
		obj, created = HalvaPoint.objects.get_or_create(uid=point.get('uid'), defaults={'name': point.get('name'),
		                                                                                'number': point.get('number')})
		if created:
			print(point.get('name'), '-> Создан')


class Command(BaseCommand):
	help = 'Generates halva points'
	
	def handle(self, *args, **options):
		# access test data
		token = settings.DATA['DevToken']
		dev_url = settings.DATA['DEV_URL']
		# access prod  data
		prod_token = settings.DATA['Token']
		prod_url = settings.DATA['PROD_URL']
		
		response_test = send_request(token, dev_url + 'terminals/?limit=1500', '')
		# get list terminals
		response_prod = send_request(prod_token, prod_url + 'terminals/?limit=1500', '')
		
		try:
			results = response_prod.json()['results']
			update_or_create_halva_points(results)
		except:
			print('Error get list terminals')
		# print(results, token, dev_url)

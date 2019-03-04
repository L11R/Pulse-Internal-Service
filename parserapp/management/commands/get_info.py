from django.core.management.base import BaseCommand
#from ...models import Points, Gallery, Coordinates, Structured_address
#from django.core.files.storage import default_storage
from django.conf import settings
from core.client import make_api_request
from json.decoder import JSONDecodeError
from core.models import Cars

import unicodedata

class Command(BaseCommand):
	help = 'Generates Fake data'
	
	def handle(self, *args, **options):
		get_request = make_api_request()
		if get_request.status_code in (200, 201):
			try:
				message = get_request.json()
			except JSONDecodeError:
				return get_request.text
		if 'message' in locals():
			items = message.get('items')
			for item in items:
				id = item.get('id')
				try:
					car = Cars.objects.get(idd=id)
				except Cars.DoesNotExist:
					n_car = Cars()
					n_car.idd = item.get('id')
					n_car.url = item.get('url')[:250]
					n_car.category = item.get('category')
					n_car.hasDamage = item.get('hasDamage')
					n_car.price = unicodedata.normalize("NFKD", item.get('price').get('grs').get('localized'))
					n_car.title = item.get('title')
					n_car.created = item.get('created')
					n_car.modified = item.get('modified')
					n_car.renewed = item.get('renewed')
					n_car.features = ';'.join([unicodedata.normalize("NFKD", word) for word in item.get('features')])[
					                 :750]
					n_car.details = ';'.join([unicodedata.normalize("NFKD", word) for word in item.get('details')])[
					                :750]
					n_car.attr = str(item.get('attr'))[:750]
					n_car.save()
				

				
				
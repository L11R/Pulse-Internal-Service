from django.core.management.base import BaseCommand
from parserapp.models import OzonPoints, AreaList
from json.decoder import JSONDecodeError
from parserapp.management.commands.get_ozon_points import get_ozon_points


import unicodedata

class Command(BaseCommand):
	help = 'Generates Fake data'
	
	def handle(self, *args, **options):
		areas_update = AreaList.objects.filter(need_update=True)

		for area in areas_update:
			data = get_ozon_points(area.idd)
			if isinstance(data, list):
				OzonPoints.update_points(data, area)
				


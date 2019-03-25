from django.core.management.base import BaseCommand
from parserapp.models import OzonPoints, AreaList
from json.decoder import JSONDecodeError
from parserapp.management.commands.get_ozon_points import get_ozon_points
import time


def repeat_update(area):
	data = get_ozon_points(area.idd)
	for g in range(3):
		if isinstance(data, list):
			OzonPoints.update_points(data, area)
			break
		else:
			data = get_ozon_points(area.idd)
		time.sleep(10)
	
import unicodedata

class Command(BaseCommand):
	help = 'Generates Fake data'
	
	def handle(self, *args, **options):
		areas_update = AreaList.objects.filter(need_update=True)

		for area in areas_update:
			repeat_update(area)
			# data = get_ozon_points(area.idd)
			# if isinstance(data, list):
			# 	OzonPoints.update_points(data, area)
			


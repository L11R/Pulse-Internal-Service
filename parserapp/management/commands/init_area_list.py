from django.core.management.base import BaseCommand

from parserapp.models import AreaList
from parserapp.data import area_list


class Command(BaseCommand):
	help = 'Generates Fake data'
	
	def handle(self, *args, **options):
		for area in area_list:
			AreaList.objects.get_or_create(idd=area.get('areaId'),
			                               defaults={"city": area.get('city')})

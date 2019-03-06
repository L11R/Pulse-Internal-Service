from django.template import loader
from django.http import HttpResponse, JsonResponse
from parserapp.models import OzonPoints, AreaList

from parserapp.management.commands.get_ozon_points import get_ozon_points


def hascyr(s):
	lower = set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')
	return lower.intersection(s.lower()) != set()


def render_page_points(request):
	params = {}
	if request.method == 'GET' and len(request.GET):
		params = {'{}__icontains'.format(k): v for k, v in request.GET.items()}
	template = loader.get_template('points.html')
	points = OzonPoints.objects.filter(**params)
	
	# part1 = OzonPoints.objects.all()[0:999]
	# part2 = OzonPoints.objects.all()[999:1998]
	# payt_list = list()
	# payt_list += list(part1)
	# payt_list += list(part2)
	
	return HttpResponse(template.render({'Points': points}, request))


def update_list_points(request):
	import transliterate
	
	update_list, response = [], {}
	areaId, city = request.GET.get('areaId', None), request.GET.get('city', None)
	if request.method == 'GET' and areaId and city:
		obj, created = AreaList.objects.update_or_create(idd=areaId, defaults={"city": city})
		if created:
			response.update({"Successfully added point number: ": areaId})
		else:
			response.update({"Successfully update point number: ": areaId})
	area_list = AreaList.objects.all()
	OzonPoints.objects.all().delete()
	for area in area_list:
		data = get_ozon_points(area.idd)
		if isinstance(data, list):
			stat_data = OzonPoints.update_points(data)
			stat_data.update({'city': transliterate.translit(area.city, reversed=True) if area.city != '' and not hascyr(area.city) else ''})
			stat_data.update({'areaId': area.idd})
			update_list.append(stat_data)
		else:
			update_list.append(data)
	response.update({'Successfully update points': update_list})
	return JsonResponse(response, safe=False)

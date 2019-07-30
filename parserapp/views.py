from django.template import loader
from django.http import HttpResponse, JsonResponse
from django.core.cache import cache

from parserapp.models import OzonPoints, AreaList
from Signin.views import login_required
from parserapp.management.commands.get_ozon_points import get_ozon_points


def hascyr(s):
	lower = set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')
	return lower.intersection(s.lower()) != set()


def get_points():
	pass


@login_required
def render_page_ozon_areas(request):
	cache.clear()
	template = loader.get_template('ozon_areas.html')
	areas = AreaList.objects.filter(visibility=True)
	return HttpResponse(template.render({'Areas': areas}, request))


@login_required
def render_page_points(request):
	params = {}
	if request.method == 'GET' and len(request.GET):
		params = {'{}__icontains'.format(k): v for k, v in request.GET.items()}
	#params['name__icontains'] = 'PonyExpress'
	params['visibility'] = True
	template = loader.get_template('ozon_points.html')
	points = OzonPoints.objects.filter(**params)
	
	# part1 = OzonPoints.objects.all()[0:999]
	# part2 = OzonPoints.objects.all()[999:1998]
	# payt_list = list()
	# payt_list += list(part1)
	# payt_list += list(part2)
	
	return HttpResponse(template.render({'Points': points}, request))


def adding_city(request):
	response = {}
	areaId = request.GET.get('areaId', None)
	city = request.GET.get('city', None)
	if request.method == 'GET' and city and areaId:
		obj, created = AreaList.objects.update_or_create(idd=areaId, defaults={"city": city, "need_update": True})
		if created:
			response.update({"Successfully added point number: {}, city: {}".format(areaId, city): 201})
			return JsonResponse(response, safe=False)
		else:
			return JsonResponse({"Error": "already exists areaId with num {}".format(areaId)}, safe=False)
	else:
		return JsonResponse({"Error in {}, {}".format(city, areaId): "Error"}, safe=False)


def update_list_points(request):
	#import transliterate
	cache.clear()
	#update_list, response = [], {}
	areaId = request.GET.get('areaId', None)
	if request.method == 'GET':
		if areaId:
			try:
				area = AreaList.objects.get(idd=areaId)
				area.need_update = True
				area.save()
				return JsonResponse({'Successfully scheduled city update': area.city if area.city != '' else area.idd}, safe=False)
			except:
				return JsonResponse({'Not found area for update, sorry'}, safe=False)
		else:
			area_list = AreaList.objects.all()
			for area in area_list:
				area.need_update = True
				area.save()
			return JsonResponse({'Successfully scheduled points': 'All'}, safe=False)
	return JsonResponse({'Error': "request method {} not allowed".format(request.method)}, safe=False)

# obj, created = AreaList.objects.update_or_create(idd=areaId, defaults={"city": city})
# if created:
# 	response.update({"Successfully added point number: ": areaId})
# else:
# 	response.update({"Successfully update point number: ": areaId})
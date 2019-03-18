from django.db import models
from datetime import datetime


class OzonPoints(models.Model):
	idd = models.IntegerField(null=True, verbose_name='Id')
	name = models.CharField(max_length=250, verbose_name='name')
	address = models.CharField(max_length=250, verbose_name='address')
	deliveryType = models.CharField(max_length=250, verbose_name='deliveryType')
	metro = models.CharField(max_length=250, verbose_name='metro')
	area = models.ForeignKey('AreaList', on_delete=models.CASCADE, blank=None, null=True)
	
	@classmethod
	def update_points(cls, data, area):
		# TODO: make check if not null data | check data
		OzonPoints.objects.filter(area=area).delete()
		
		count = 0
		
		for i in data:
			point, create = cls.objects.get_or_create(idd=i.get('id'), defaults={"name": i.get('name')[:250],
			                                                                     "address": i.get('address')[:250],
			                                                                     "area": area})
			if create:
				count += 1
				try:
					point.metro = i.get('metro')[:250]
					point.save()
				except:
					print('Error create metro')
		area.last_points_count = area.points_count
		area.update_at = datetime.now()
		area.points_count = count
		area.need_update = False
		area.save()
		


class AreaList(models.Model):
	idd = models.IntegerField(verbose_name='idd')
	city = models.CharField(max_length=250, verbose_name='city')
	update_at = models.DateTimeField(auto_now=True)
	last_points_count = models.IntegerField(default=0, verbose_name='last_points_count')
	points_count = models.IntegerField(default=0, verbose_name='points_count')
	need_update = models.BooleanField(default=False, verbose_name='need_update')

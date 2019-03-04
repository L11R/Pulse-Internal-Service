from django.db import models


class OzonPoints(models.Model):
	idd = models.IntegerField(null=True, verbose_name='Id')
	name = models.CharField(max_length=250, verbose_name='name')
	address = models.CharField(max_length=250, verbose_name='address')
	deliveryType = models.CharField(max_length=250, verbose_name='deliveryType')
	metro = models.CharField(max_length=250, verbose_name='metro')
	
	@classmethod
	def update_points(cls, data):
		count = 0
		for i in data:
			point, create = cls.objects.get_or_create(idd=i.get('id'), defaults={"name": i.get('name')[:250],
				"address": i.get('address')[:250]})
			if create:
				count += 1
				try:
					point.metro = i.get('metro')[:250]
					point.save()
				except:
					print('Error create metro')
		return {"added": count}


class AreaList(models.Model):
	idd = models.IntegerField(verbose_name='idd')
	city = models.CharField(max_length=250, verbose_name='city')

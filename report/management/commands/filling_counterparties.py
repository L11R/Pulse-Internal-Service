# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from Signin import models
import csv

class Command(BaseCommand):
    help = 'Creates and sends report on consignors from Information System'
    
    def handle(self, *args, **options):
        with open("counterpartie.csv", encoding='cp1251') as file:
            reader = csv.DictReader(file, delimiter=";")
            count = 0
            for row in reader:
                if row['№ ']:
                    count +=1
                    model = models.Сounterparty()
                    model.address_point = row['Адрес объекта']
                    model.number_point = row['№ ']
                    model.entity = row['Юр. лицо']
                    model.save()
                    print(row['Адрес объекта'], row['Юр. лицо'], row['№ '], '---', count)
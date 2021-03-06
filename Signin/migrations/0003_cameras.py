# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-05-04 16:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Signin', '0002_auto_20180503_1043'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cameras',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=128, verbose_name='URL камеры')),
                ('number', models.IntegerField(verbose_name='Номер камеры')),
                ('name', models.CharField(max_length=128, verbose_name='Наименование камеры')),
            ],
            options={
                'verbose_name': 'Камера',
                'verbose_name_plural': 'Камеры',
            },
        ),
    ]

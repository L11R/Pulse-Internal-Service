# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-03-18 21:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Signin', '0019_auto_20190318_2111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cameras',
            name='stype',
            field=models.SmallIntegerField(choices=[(0, '197.1.102.XX'), (1, '172.28.2.XX')], default=0, verbose_name='Тип'),
        ),
    ]

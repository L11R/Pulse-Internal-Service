# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-03-18 02:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Signin', '0013_auto_20190318_0217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cameras',
            name='stype',
            field=models.SmallIntegerField(choices=[(0, '197.1.102.XX'), (1, '172.28.2.XX')], default=0, verbose_name='Тип'),
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-08-02 13:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Signin', '0005_cameras_stype'),
    ]

    operations = [
        migrations.CreateModel(
            name='Сounterparty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_point', models.IntegerField(verbose_name='Номер точки')),
                ('address_point', models.CharField(max_length=256, verbose_name='Адрес точки')),
                ('entity', models.CharField(max_length=256, verbose_name='Юр лицо')),
            ],
            options={
                'verbose_name': 'Контрагент',
                'verbose_name_plural': 'Контрагенты',
            },
        ),
        migrations.AlterField(
            model_name='cameras',
            name='stype',
            field=models.SmallIntegerField(choices=[(0, '197.1.102.XX'), (1, '172.28.2.XX')], default=0, verbose_name='Тип'),
        ),
    ]

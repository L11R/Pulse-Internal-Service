# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2019-02-26 15:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.UUIDField(editable=False, primary_key=True, serialize=False, verbose_name='UID сообщения')),
                ('date_modified', models.DateTimeField(blank=True, null=True, verbose_name='Дата модификации')),
                ('meta', models.CharField(blank=True, default='', max_length=550, null=True, verbose_name='Дополнительные данные')),
                ('order_id', models.CharField(blank=True, default='', max_length=64, null=True, verbose_name='Клиентский номер')),
                ('barcodes', models.CharField(blank=True, default='', max_length=150, null=True, verbose_name='Штрихкоды')),
                ('order_status', models.SmallIntegerField(choices=[(0, 'Создана'), (1, 'Ожидает приёмки'), (2, 'В доставке'), (3, 'Доставлена'), (4, 'Выдана'), (5, 'Просрочена'), (6, 'Забрана на возврат'), (7, 'На хранении'), (8, 'На возврате'), (9, 'Возвращена'), (10, 'Проблемная'), (11, 'Техническая проблема'), (12, 'Отменена'), (13, 'Хранение продлено клиентом'), (14, 'Объявлена'), (15, 'Хранится'), (16, 'Готово к получению'), (17, 'Получено'), (18, 'Готово к изъятию'), (19, 'Изъято')], default=0, verbose_name='Статус отправления')),
                ('msg_status', models.SmallIntegerField(choices=[(0, 'Новое'), (1, 'Отправлено'), (2, 'Запланировано'), (3, 'Не отправлено'), (4, 'Техническая проблема')], default=0, verbose_name='Статус сообщения')),
            ],
            options={
                'verbose_name': 'Сообщение',
                'verbose_name_plural': 'Сообщения',
                'ordering': ('-date_modified',),
            },
        ),
        migrations.CreateModel(
            name='MessageStat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now=True, verbose_name='Дата')),
                ('sent', models.SmallIntegerField(blank=True, default=0, null=True, verbose_name='Отправленно')),
                ('unsent', models.SmallIntegerField(blank=True, default=0, null=True, verbose_name='Не отправленно')),
                ('problem', models.SmallIntegerField(blank=True, default=0, null=True, verbose_name='Проблемных')),
                ('new', models.SmallIntegerField(blank=True, default=0, null=True, verbose_name='Новых')),
                ('planned', models.SmallIntegerField(blank=True, default=0, null=True, verbose_name='Запланированных')),
            ],
            options={
                'verbose_name': 'Статистика',
            },
        ),
        migrations.CreateModel(
            name='Operation',
            fields=[
                ('idd', models.UUIDField(editable=False, primary_key=True, serialize=False, verbose_name='UID события')),
                ('otype', models.CharField(max_length=32, verbose_name='Тип операции')),
                ('dt', models.DateTimeField(verbose_name='Дата и время операции UTC')),
                ('courier_name', models.CharField(max_length=256, null=True, verbose_name='Курьер, совершивший операцию')),
                ('courier_login', models.CharField(max_length=32, null=True, verbose_name='Логин курьера, совершившего операцию')),
                ('cell', models.CharField(max_length=3, verbose_name='Название ячейки')),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('idd', models.CharField(default=uuid.uuid4, max_length=255, primary_key=True, serialize=False, unique=True)),
                ('order_id', models.CharField(max_length=64, verbose_name='Клиентский номер')),
                ('barcodes', models.CharField(max_length=256, verbose_name='Баркод')),
                ('terminal', models.CharField(max_length=8, verbose_name='Номер')),
                ('point_settlement', models.CharField(max_length=128, verbose_name='Населенный пункт')),
                ('point_address', models.TextField(verbose_name='Адрес')),
                ('dpd_point_code', models.CharField(blank=True, default='', editable=False, max_length=32)),
                ('consignor', models.CharField(default='', max_length=128, verbose_name='Отправитель')),
                ('date_added', models.DateTimeField(null=True, verbose_name='Дата создания')),
                ('date_delivered', models.DateTimeField(blank=True, null=True, verbose_name='Время закладки')),
                ('date_received', models.DateTimeField(blank=True, null=True, verbose_name='Время получения')),
                ('date_backout', models.DateTimeField(blank=True, null=True, verbose_name='Время забора на возврат')),
                ('expire_at', models.DateTimeField(blank=True, null=True, verbose_name='Дата истечения срока хранения')),
                ('status', models.SmallIntegerField(choices=[(0, 'Создана'), (1, 'Ожидает приёмки'), (2, 'В доставке'), (3, 'Доставлена'), (4, 'Выдана'), (5, 'Просрочена'), (6, 'Забрана на возврат'), (7, 'На хранении'), (8, 'На возврате'), (9, 'Возвращена'), (10, 'Проблемная'), (11, 'Техническая проблема'), (12, 'Отменена'), (13, 'Хранение продлено клиентом'), (14, 'Объявлена'), (15, 'Хранится'), (16, 'Готово к получению'), (17, 'Получено'), (18, 'Готово к изъятию'), (19, 'Изъято')], default=0, verbose_name='Статус')),
                ('cod', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Наложенный платёж')),
                ('partner_service_fee', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Цена услуг партнёра')),
                ('declared_price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Объявленная ценность')),
                ('phone', models.CharField(max_length=20, verbose_name='Телефон')),
                ('sender', models.CharField(max_length=128, verbose_name='Контрагент')),
                ('timezone', models.CharField(default=None, max_length=32, null=True, verbose_name='Часовой пояс точки')),
                ('delivery_registry', models.CharField(blank=True, default='', max_length=15, null=True, verbose_name='Номер реестра закладки')),
                ('backout_registry', models.CharField(blank=True, default='', max_length=156, null=True, verbose_name='Номер реестра выемки')),
                ('size', models.SmallIntegerField(choices=[(0, 'XS'), (1, 'S'), (2, 'M'), (3, 'L'), (4, 'XL'), (5, 'S/2'), (6, 'M/2')], default=1, verbose_name='Типоразмер')),
            ],
            options={
                'verbose_name': 'Отчёт',
                'verbose_name_plural': 'Отчёты',
            },
        ),
        migrations.AddField(
            model_name='operation',
            name='report',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='report.Report', verbose_name='Запись о посылке'),
        ),
    ]

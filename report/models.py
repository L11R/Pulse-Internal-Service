from django.db import models
from uuid import uuid4


PARCEL_STATUS_CHOICES = {
    (0, 'Создана'),
    (1, 'Ожидает приёмки'),
    (2, 'В доставке'),
    (3, 'Доставлена'),
    (4, 'Выдана'),
    (5, 'Просрочена'),
    (6, 'Забрана на возврат'),
    (7, 'На хранении'),
    (8, 'На возврате'),
    (9, 'Возвращена'),
    (10, 'Проблемная'),
    (11, 'Техническая проблема'),
    (12, 'Отменена'),
    (13, 'Хранение продлено клиентом'),
}


class Report(models.Model):
    """
    Отчётность
    """
    # should be parcel uid
    idd = models.CharField(max_length=255, unique=True, primary_key=True, default=uuid4)
    order_id = models.CharField(max_length=64, editable=True, verbose_name="Клиентский номер")
    barcodes = models.CharField(max_length=256, verbose_name="Баркод")
    terminal = models.CharField(max_length=8, verbose_name="Номер")
    point_settlement = models.CharField(max_length=128, verbose_name="Населенный пункт")
    point_address = models.TextField(verbose_name="Адрес")
    dpd_point_code = models.CharField(max_length=32, editable=False, blank=True, default="")
    consignor = models.CharField(max_length=128, default='', verbose_name='Отправитель')
    date_added = models.DateTimeField(null=True, verbose_name="Дата создания")
    status = models.SmallIntegerField(choices=PARCEL_STATUS_CHOICES, default=0, verbose_name="Статус")
    cod = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Наложенный платёж")
    partner_service_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0,
                                              verbose_name="Цена услуг партнёра")
    declared_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Объявленная ценность")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    sender = models.CharField(max_length=128, verbose_name="Контрагент")

    class Meta:
        db_table = "reports"
        verbose_name = 'Отчёт'
        verbose_name_plural = 'Отчёты'


class Operation(models.Model):
    idd = models.UUIDField(primary_key=True, editable=False, verbose_name='UID события')
    report = models.ForeignKey(Report, verbose_name="Запись о посылке")
    otype = models.CharField(max_length=32, verbose_name='Тип операции')
    dt = models.DateTimeField(verbose_name='Дата и время операции UTC')
    courier_name = models.CharField(max_length=256, null=True, verbose_name='Курьер, совершивший операцию')
    courier_login = models.CharField(max_length=32, null=True, verbose_name='Логин курьера, совершившего операцию')
    cell = models.CharField(max_length=3, verbose_name='Название ячейки')
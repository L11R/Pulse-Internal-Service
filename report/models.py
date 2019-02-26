from django.db import models
from uuid import uuid4
from .choices import MESSAGE_STATUS_CHOICES

def _rev_dict(choices):
    return {v:k for k, v in choices}

CELL_SIZE_CHOICE = (
    (0, 'XS'),
    (1, 'S'),
    (2, 'M'),
    (3, 'L'),
    (4, 'XL'),
    (5, 'S/2'),
    (6, 'M/2'))
CELL_SIZE_REV_DICT = _rev_dict(CELL_SIZE_CHOICE)
CELL_SIZE_DICT = {k:v for k,v in CELL_SIZE_CHOICE}

MESSAGE_STATUS_CHOICES = (
    (0, 'Новое'),
    (1, 'Отправлено'),
    (2, 'Запланировано'),
    (3, 'Не отправлено'),
    (4, 'Техническая проблема'))

PARCEL_STATUS_CHOICES = (
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
    (13, 'Хранение продлено клиентом'), # bailment statuses
    (14, 'Объявлена'),
    (15, 'Хранится'),
    (16, 'Готово к получению'),
    (17, 'Получено'),
    (18, 'Готово к изъятию'),
    (19, 'Изъято'))


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
    date_delivered = models.DateTimeField(null=True, blank=True, verbose_name='Время закладки')
    date_received = models.DateTimeField(null=True, blank=True, verbose_name='Время получения')
    date_backout = models.DateTimeField(null=True, blank=True, verbose_name='Время забора на возврат')
    expire_at = models.DateTimeField(blank=True, null=True, editable=True, verbose_name="Дата истечения срока хранения")
    status = models.SmallIntegerField(choices=PARCEL_STATUS_CHOICES, default=0, verbose_name="Статус")
    cod = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Наложенный платёж")
    partner_service_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0,
                                              verbose_name="Цена услуг партнёра")
    declared_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Объявленная ценность")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    sender = models.CharField(max_length=128, verbose_name="Контрагент")
    timezone = models.CharField(max_length=32, null=True, default=None, verbose_name="Часовой пояс точки")
    delivery_registry = models.CharField(max_length=15, null=True, blank=True, default="",
                                         verbose_name='Номер реестра закладки')
    backout_registry = models.CharField(max_length=156, null=True, blank=True, default="",
                                        verbose_name='Номер реестра выемки')
    size = models.SmallIntegerField(choices=CELL_SIZE_CHOICE, default=1, verbose_name="Типоразмер")

    class Meta:
        verbose_name = 'Отчёт'
        verbose_name_plural = 'Отчёты'

    @property
    def api_status(self):
        return self.get_status_display()

    @property
    def api_size(self):
        return self.get_size_display()


class Operation(models.Model):
    idd = models.UUIDField(primary_key=True, editable=False, verbose_name='UID события')
    report = models.ForeignKey(Report, verbose_name="Запись о посылке")
    otype = models.CharField(max_length=32, verbose_name='Тип операции')
    dt = models.DateTimeField(verbose_name='Дата и время операции UTC')
    courier_name = models.CharField(max_length=256, null=True, verbose_name='Курьер, совершивший операцию')
    courier_login = models.CharField(max_length=32, null=True, verbose_name='Логин курьера, совершившего операцию')
    cell = models.CharField(max_length=3, verbose_name='Название ячейки')


class Message(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, verbose_name='UID сообщения')
    date_modified = models.DateTimeField(blank=True, null=True, verbose_name="Дата модификации")
    meta = models.CharField(default="", max_length=550, null=True, blank=True, verbose_name="Дополнительные данные")
    order_id = models.CharField(default="", max_length=64, null=True, blank=True, verbose_name="Клиентский номер")
    barcodes = models.CharField(default="", max_length=150, null=True, blank=True, verbose_name="Штрихкоды")
    order_status = models.SmallIntegerField(choices=PARCEL_STATUS_CHOICES, default=0, verbose_name="Статус отправления")
    msg_status = models.SmallIntegerField(choices=MESSAGE_STATUS_CHOICES, default=0, verbose_name="Статус сообщения")

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ("-date_modified",)

    @property
    def api_order_status(self):
        return self.get_order_status_display()

    @property
    def api_msg_status(self):
        return self.get_msg_status_display()

    def __str__(self):
        return 'Сообщение {} по номеру заказа №{}'.format(self.id, self.order_id)


class MessageStat(models.Model):
    date = models.DateField(auto_now=True, verbose_name="Дата")
    sent = models.SmallIntegerField(null=True, blank=True, default=0, verbose_name="Отправленно")
    unsent = models.SmallIntegerField(null=True, blank=True, default=0, verbose_name="Не отправленно")
    problem = models.SmallIntegerField(null=True, blank=True, default=0, verbose_name="Проблемных")
    new = models.SmallIntegerField(null=True, blank=True, default=0, verbose_name="Новых")
    planned = models.SmallIntegerField(null=True, blank=True, default=0, verbose_name="Запланированных")

    class Meta:
        verbose_name = 'Статистика'


class TerminalCapacity(models.Model):
    station_id = models.CharField(max_length=8, verbose_name='Номер станции')
    dt = models.DateTimeField(verbose_name='Дата и время проверки')
    occupancy = models.IntegerField('Заполненность')

    class Meta:
        db_table = "ADM_capacity"
        verbose_name = 'Вместимость терминала'
        verbose_name_plural = 'Вместимость терминалов'
		


from django.db import models
from uuid import uuid4

MESSAGE_STATUS_CHOICES = (
    (0, 'Новое'),
    (1, 'Отправлено'),
    (2, 'Запланировано'),
    (3, 'Не отправлено'),
    (4, 'Техническая проблема'))
# Create your models here.
class Sms(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, verbose_name='UID сообщения')
    date_modified = models.DateTimeField(blank=True, null=True, verbose_name="Дата модификации")
    meta = models.CharField(max_length=550, null=True, blank=True, default="", verbose_name="Дополнительные данные")
    order_id = models.CharField(max_length=64, null=True, blank=True, default="", verbose_name="Клиентский номер")
    barcodes = models.CharField(max_length=150, null=True, blank=True, default="", verbose_name="Штрихкоды")
    order_status = models.CharField(max_length=150, null=True, blank=True, default="", verbose_name="Статус отправления")
    msg_status = models.SmallIntegerField(choices=MESSAGE_STATUS_CHOICES,  default=0,
                                      verbose_name="Статус сообщения")
    class Meta:
        db_table = "sms"
        verbose_name = 'Смс'
        verbose_name_plural = 'Смсы'
        ordering = ("-date_modified",)

class Statistics_msg(models.Model):
    id = models.CharField(max_length=255, unique=True, primary_key=True, default=uuid4)
    date = models.DateTimeField(blank=True, null=True, verbose_name="Дата")
    sent_msg = models.SmallIntegerField(null=True, blank=True, default=0, verbose_name="Отправленых")
    no_sent_msg = models.SmallIntegerField(null=True, blank=True, default=0, verbose_name="Не отправленых")
    techn_problem = models.SmallIntegerField(null=True, blank=True, default=0, verbose_name="Техническая проблема")
    new_msg = models.SmallIntegerField(null=True, blank=True, default=0, verbose_name="Новых сообщений")
    planned_msg = models.SmallIntegerField(null=True, blank=True, default=0, verbose_name="Запланированных сообщений")
    
    class Meta:
        db_table = "statistics_msg"
        verbose_name = 'статистика'
        verbose_name_plural = 'статистики'
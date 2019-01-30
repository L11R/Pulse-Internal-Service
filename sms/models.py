from django.db import models

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
    meta = models.CharField(max_length=150, null=True, blank=True, default="", verbose_name="Дополнительные данные")
    order_id = models.CharField(max_length=64, null=True, blank=True, default="", verbose_name="Клиентский номер")
    barcodes = models.CharField(max_length=150, null=True, blank=True, default="", verbose_name="Штрихкоды")
    order_status = models.CharField(max_length=150, null=True, blank=True, default="", verbose_name="Статус отправления")
    msg_status = models.SmallIntegerField(choices=MESSAGE_STATUS_CHOICES,  default=0,
                                      verbose_name="Статус сообщения")
    class Meta:
        db_table = "sms"
        verbose_name = 'Смс'
        verbose_name_plural = 'Смсы'
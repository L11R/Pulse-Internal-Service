from django.db import models

USER_TYPE_CHOICES = (
    (0, "SERVICES"),
    (1, "SENDER"),
)
CAMERAS_TYPE_CHOICES = {
    (0, "197.1.102.XX"),
    (1, "172.28.2.XX"),
}

class Сounterparty(models.Model):
    number_point = models.IntegerField(verbose_name="Номер точки")
    address_point = models.CharField(max_length=256, verbose_name='Адрес точки')
    entity = models.CharField(max_length=256, verbose_name="Юр лицо")
    class Meta:
        verbose_name = "Контрагент"
        verbose_name_plural = "Контрагенты"

class Sender(models.Model):
    name = models.CharField(max_length=64, verbose_name="Имя отправителя")
    token = models.CharField(max_length=128, verbose_name="Токен")
    uid = models.CharField(max_length=64, verbose_name="UUID")
    
    def publish(self):
        self.save()
        
    def __str__(self):
        return 'Отправитель {}'.format(self.name)
    
class Users(models.Model):
    username = models.CharField(max_length=64, verbose_name="Логин")
    password = models.CharField(max_length=128, verbose_name="Пароль")
    email = models.EmailField(null=True, verbose_name="Email")
    stype = models.SmallIntegerField(choices=USER_TYPE_CHOICES, verbose_name="Тип")
    
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.get_name()

    def get_name(self):
        return 'Пользователь {}'.format(self.username)
    
    @property
    def api_type(self):
        return self.get_stype_display()
    
class Cameras(models.Model):
    url = models.CharField(max_length=256, verbose_name="URL камеры")
    number = models.IntegerField(verbose_name="Номер камеры")
    name = models.CharField(max_length=128, verbose_name="Наименование камеры")
    stype = models.SmallIntegerField(choices=CAMERAS_TYPE_CHOICES, default=0, verbose_name="Тип")
    
    class Meta:
        verbose_name = "Камера"
        verbose_name_plural = "Камеры"
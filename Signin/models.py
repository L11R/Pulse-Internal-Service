from django.db import models

class Sender(models.Model):
    name = models.CharField(max_length=64, verbose_name="Имя отправителя")
    token = models.CharField(max_length=128, verbose_name="Пароль")
    uid = models.CharField(max_length=64, verbose_name="UUID")
    
    def publish(self):
        self.save()
    def __str__(self):
        return self.name
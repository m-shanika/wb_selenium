from django.db import models
import json

class Accounts(models.Model):
    SEX = (
        ('FEMALE', 'Female'),
        ('MALE', 'Male')
    )
    session = models.TextField(verbose_name="Сессия")
    phone_number = models.CharField(verbose_name="Номер", max_length=20)
    sex = models.CharField(verbose_name="Пол", max_length=15, choices = SEX)
    first_name = models.CharField(verbose_name="Имя",max_length=50)
    last_name = models.CharField(verbose_name="Фамилия",max_length=50)
    cookies = models.TextField(verbose_name="Куки")
    token = models.TextField(verbose_name="Токен")
    is_buy = models.BooleanField(verbose_name="Покупал", default=False)
        
    class Meta:
        verbose_name = "Аккаунт"
        verbose_name_plural = "Аккаунты"

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.phone_number}"    
    
    def save(self, *args, **kwargs):
        if isinstance(self.cookies, list):
            self.cookies = json.dumps(self.cookies)
        super().save(*args, **kwargs)
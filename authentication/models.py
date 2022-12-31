from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.db import models


class Location(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')
    lat = models.FloatField(max_length=50, verbose_name='Широта', null=True, blank=True)
    lng = models.FloatField(max_length=50, verbose_name='Долгота', null=True, blank=True)

    class Meta:
        verbose_name = 'Локация'
        verbose_name_plural = 'Локации'

    def __str__(self):
        return self.name


class User(AbstractUser):
    STATUS = [
        ('member', 'участник'),
        ('moderator', 'модератор'),
        ('admin', 'админ')
    ]

    role = models.CharField(max_length=9, choices=STATUS, verbose_name='Роль')
    age = models.IntegerField(verbose_name='Возраст', blank=True, null=True)
    locations = models.ManyToManyField(Location, verbose_name='Локация', blank=True)
    birth_date = models.DateField(verbose_name='дата рождения', default='1990-01-01')
    email = models.EmailField(unique=True, verbose_name='email')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'



    def __str__(self):
        return self.username


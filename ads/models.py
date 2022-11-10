from django.db import models


class Advertisement(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')
    author = models.CharField(max_length=150, verbose_name='Автор')
    price = models.IntegerField(verbose_name='Цена')
    description = models.TextField(verbose_name='Описание')
    address = models.CharField(max_length=300, verbose_name='Адресс')
    is_published = models.BooleanField(verbose_name='Опубликовано')

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'


class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

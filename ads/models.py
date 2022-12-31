from django.core.validators import MinValueValidator
from django.db import models

from ads.validators import MinLengthValidator
from authentication.models import User

NULLABLE = {'null': True, 'blank': True}


class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название')
    slug = models.CharField(max_length=10, validators=[MinLengthValidator(length=5)], unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Advertisement(models.Model):
    name = models.CharField(max_length=200, validators=[MinLengthValidator(length=10)], verbose_name='Название')
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    price = models.IntegerField(verbose_name='Цена', validators=[MinValueValidator(0)])
    description = models.TextField(verbose_name='Описание', **NULLABLE)
    is_published = models.BooleanField(verbose_name='Опубликовано', default=False)
    image = models.ImageField(upload_to='images/', verbose_name='Картинка', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'

    def __str__(self):
        return self.name


class Selection(models.Model):
    items = models.ManyToManyField(Advertisement, verbose_name='подборка', blank=True)
    name = models.CharField(max_length=200, verbose_name='название')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='автор', blank=True)

    class Meta:
        verbose_name = 'Подборка'
        verbose_name_plural = 'Подборки'

    def __str__(self):
        return self.name

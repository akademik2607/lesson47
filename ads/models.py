from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')
    lat = models.FloatField(max_length=50, verbose_name='Широта', null=True, blank=True)
    lng = models.FloatField(max_length=50, verbose_name='Долгота', null=True, blank=True)

    class Meta:
        verbose_name = 'Локация'
        verbose_name_plural = 'Локации'

    def __str__(self):
        return self.name


class User(models.Model):
    STATUS = [
        ('member', 'участник'),
        ('moderator', 'модератор'),
        ('admin', 'админ')
    ]
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    username = models.CharField(max_length=100, verbose_name='Логин')
    password = models.CharField(max_length=15, verbose_name='Пароль')
    role = models.CharField(max_length=9, choices=STATUS, verbose_name='Роль')
    age = models.IntegerField(verbose_name='Возраст')
    location = models.ManyToManyField(Location, verbose_name='Локация', blank=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Advertisement(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    price = models.IntegerField(verbose_name='Цена')
    description = models.TextField(verbose_name='Описание')
    is_published = models.BooleanField(verbose_name='Опубликовано')
    image = models.ImageField(upload_to='images/', verbose_name='Картинка', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'

    def __str__(self):
        return self.name

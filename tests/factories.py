import factory
from django.contrib.auth.hashers import make_password

from ads.models import Advertisement, Category
from authentication.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('name')
    password = make_password('test_password')
    role = 'admin'
    is_superuser = True
    email = factory.Faker('email')


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = 'Категория'
    slug = factory.Faker('word')


class AdvertisementFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Advertisement

    name = "Сибирская котята, новые"
    author = factory.SubFactory(UserFactory)
    price = 2500
    description = "Продаю сибирских котят,новых."
    is_published = False
    category = factory.SubFactory(CategoryFactory)



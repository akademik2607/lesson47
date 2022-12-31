from pytest_factoryboy import register

from tests.factories import AdvertisementFactory, UserFactory, CategoryFactory

pytest_plugins = 'tests.fixtures'

register(UserFactory)
register(CategoryFactory)
register(AdvertisementFactory)

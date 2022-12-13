from django.contrib import admin

from ads.models import Category, Advertisement
from authentication.models import User, Location

admin.site.register(Category)
admin.site.register(Location)
admin.site.register(User)
admin.site.register(Advertisement)

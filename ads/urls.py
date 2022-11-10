from django.urls import path

from ads.views import index, CategoriesView, AdvertisementsView, AdvertisementView, CategoryView

urlpatterns = [
    path('', index),
    path('cat/', CategoriesView.as_view()),
    path('ad/', AdvertisementsView.as_view()),
    path('ad/<int:aid>', AdvertisementView.as_view()),
    path('cat/<int:cid>', CategoryView.as_view())
]
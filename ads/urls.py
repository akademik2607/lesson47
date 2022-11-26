from django.urls import path
from rest_framework import routers

from ads import views


router = routers.SimpleRouter()
router.register(r'location', views.LocationViewSet)


urlpatterns = [
    path('', views.index),
    path('cat/', views.CategoriesListView.as_view()),
    path('ad/', views.AdvertisementsListView.as_view()),
    path('user/', views.UserListView.as_view()),
    path('cat/create/', views.CategoryCreateView.as_view()),
    path('ad/create/', views.AdvertisementCreateView.as_view()),
    path('user/create/', views.UserCreateView.as_view()),
    path('ad/<int:pk>/', views.AdvertisementDetailView.as_view()),
    path('cat/<int:pk>/', views.CategoryDetailView.as_view()),
    path('user/<int:pk>/', views.UserRetrieveView.as_view()),
    path('ad/<int:pk>/delete/', views.AdvertisementDeleteView.as_view()),
    path('cat/<int:pk>/delete/', views.CategoryDeleteView.as_view()),
    path('user/<int:pk>/delete/', views.UserDestroyView.as_view()),
    path('ad/<int:pk>/update/', views.AdvertisementUpdateView.as_view()),
    path('cat/<int:pk>/update/', views.CategoryUpdateView.as_view()),
    path('user/<int:pk>/update/', views.UserUpdateView.as_view()),
    path('ad/<int:pk>/upload_image/', views.AdvertisementImageUpdateView.as_view()),
]

urlpatterns += router.urls

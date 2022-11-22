from django.urls import path

from ads.views import index, CategoriesListView, AdvertisementsListView, AdvertisementDetailView, CategoryDetailView, \
    CategoryCreateView, AdvertisementCreateView, CategoryDeleteView, AdvertisementDeleteView, CategoryUpdateView, \
    AdvertisementUpdateView, AdvertisementImageUpdateView, UserListView, UserDetailView, UserUpdateView, UserCreateView, \
    UserDeleteView

urlpatterns = [
    path('', index),
    path('cat/', CategoriesListView.as_view()),
    path('ad/', AdvertisementsListView.as_view()),
    path('user/', UserListView.as_view()),
    path('cat/create/', CategoryCreateView.as_view()),
    path('ad/create/', AdvertisementCreateView.as_view()),
    path('user/create/', UserCreateView.as_view()),
    path('ad/<int:pk>/', AdvertisementDetailView.as_view()),
    path('cat/<int:pk>/', CategoryDetailView.as_view()),
    path('user/<int:pk>/', UserDetailView.as_view()),
    path('ad/<int:pk>/delete/', AdvertisementDeleteView.as_view()),
    path('cat/<int:pk>/delete/', CategoryDeleteView.as_view()),
    path('user/<int:pk>/delete/', UserDeleteView.as_view()),
    path('ad/<int:pk>/update/', AdvertisementUpdateView.as_view()),
    path('cat/<int:pk>/update/', CategoryUpdateView.as_view()),
    path('user/<int:pk>/update/', UserUpdateView.as_view()),
    path('ad/<int:pk>/upload_image/', AdvertisementImageUpdateView.as_view()),

]

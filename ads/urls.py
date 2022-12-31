from django.urls import path

from ads import views


urlpatterns = [
    path('', views.index),
    path('cat/', views.CategoriesListView.as_view()),
    # path('ads/', views.AdvertisementsListView.as_view()),
    path('ads/', views.AdvertisementCreateListView.as_view()),
    path('selection/', views.SelectionCreateListView.as_view()),
    path('cat/create/', views.CategoryCreateView.as_view()),
    path('ads/create/', views.AdvertisementCreateView.as_view()),
    path('selection/create/', views.SelectionCreateView.as_view()),
    path('ads/<int:pk>/', views.AdvertisementRetrieveView.as_view()),
    path('cat/<int:pk>/', views.CategoryDetailView.as_view()),
    path('selection/<int:pk>/', views.SelectionRetrieveView.as_view()),
    path('ads/<int:pk>/delete/', views.AdvertisementDestroyView.as_view()),
    path('cat/<int:pk>/delete/', views.CategoryDeleteView.as_view()),
    path('selection/<int:pk>/delete/', views.SelectionDestroyView.as_view()),
    path('ads/<int:pk>/update/', views.AdvertisementUpdateView.as_view()),
    path('cat/<int:pk>/update/', views.CategoryUpdateView.as_view()),
    path('selection/<int:pk>/update/', views.SelectionUpdateView.as_view()),
    path('ads/<int:pk>/upload_image/', views.AdvertisementImageUpdateView.as_view()),
]


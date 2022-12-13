from django.urls import path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from authentication import views

router = routers.SimpleRouter()
router.register(r'location', views.LocationViewSet)

urlpatterns = [
    path('', views.UserListView.as_view()),
    path('create/', views.UserCreateView.as_view()),
    path('<int:pk>/', views.UserRetrieveView.as_view()),
    path('<int:pk>/delete/', views.UserDestroyView.as_view()),
    path('<int:pk>/update/', views.UserUpdateView.as_view()),
    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view())
]


from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from authentication.models import User, Location
from authentication.serializers import UserGetSerializer, UserCreateSerializer, UserUpdateSerializer, \
    LocationSetSerializer


class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserGetSerializer
    permission_classes = [IsAuthenticated]


class UserRetrieveView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserGetSerializer


class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer


class UserUpdateView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer


class UserDestroyView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserGetSerializer


class LocationViewSet(ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSetSerializer

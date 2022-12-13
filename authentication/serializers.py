
from rest_framework import serializers

from authentication.models import User,Location


class UserCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False, read_only=True)
    locations = serializers.SlugRelatedField(
        required=False,
        many=True,
        slug_field='name',
        queryset=Location.objects.all()
    )

    class Meta:
        model = User
        fields = '__all__'

    def is_valid(self, raise_exception=False):
        self._locations = self.initial_data.pop('locations')

        return super().is_valid(raise_exception=raise_exception)

    def create(self, validate_data):
        user = super().create(validate_data)
        for location in self._locations:
            loc_data, _ = Location.objects.get_or_create(name=location)
            user.locations.add(loc_data)
        user.save()

        return user


class UserGetSerializer(serializers.ModelSerializer):
    locations = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name',
    )

    class Meta:
        model = User
        fields = '__all__'


class UserUpdateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False, read_only=True)
    locations = serializers.SlugRelatedField(
        many=True,
        queryset=Location.objects.all(),
        slug_field='name',
    )
    class Meta:
        model = User
        fields = '__all__'

    def is_valid(self, raise_exception=False):
        self._locations = self.initial_data.pop('locations')

        return super().is_valid(raise_exception=raise_exception)

    def save(self):
        user = super().save()
        for location in self._locations:
            loc_data, _ = Location.objects.get_or_create(name=location)
            user.locations.add(loc_data)
        user.save()

        return user


class LocationSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

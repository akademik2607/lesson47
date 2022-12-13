from rest_framework import serializers

from ads.models import Category, Advertisement, Selection
from authentication.models import User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class AdvertisementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertisement
        fields = '__all__'


class SelectionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Selection
        fields = ['id', 'name']


class SelectionRetrieveSerializer(serializers.ModelSerializer):
    items = AdvertisementSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Selection
        fields = '__all__'


class SelectionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Selection
        exclude = ['owner']

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user

        return super().create(validated_data)

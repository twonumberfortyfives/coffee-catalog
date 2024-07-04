from rest_framework import serializers

from restaurant_search.models import Restaurant, Image


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = "__all__"


class RestaurantListSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Restaurant
        fields = ("id", "unique_id", "name", "address", "opening_hours", "images")


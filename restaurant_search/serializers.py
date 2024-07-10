from restaurant_search.models import Restaurant, Review, Image
from rest_framework import serializers


class ImageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = "__all__"


class ReviewListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"


class RestaurantListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = "__all__"


class RestaurantDetailSerializer(serializers.ModelSerializer):
    reviews = ReviewListSerializer(many=True, read_only=True)
    images = ImageListSerializer(many=True, read_only=True)

    class Meta:
        model = Restaurant
        fields = "__all__"

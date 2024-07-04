from django.contrib.auth import get_user_model
from rest_framework import serializers

from restaurant_search.models import Restaurant, Image, Comment


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = "__all__"


class UserForCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("id", "email")


class CommentListSerializer(serializers.ModelSerializer):
    user = UserForCommentSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ("id", "content", "restaurant", "user")


class RestaurantListSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)
    comments = CommentListSerializer(many=True, read_only=True)

    class Meta:
        model = Restaurant
        fields = ("id", "unique_id", "name", "address", "opening_hours", "images", "comments")

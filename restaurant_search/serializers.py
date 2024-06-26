from rest_framework import serializers

from restaurant_search.models import Restaurant


class RestaurantListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = "__all__"

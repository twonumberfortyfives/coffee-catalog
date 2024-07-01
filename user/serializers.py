from django.contrib.auth import get_user_model
from rest_framework import serializers

from user.models import Favourite


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "password",
            "is_verified",
            "tokens",
        )
        read_only_fields = ("id", "is_staff", "is_verified")
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = get_user_model()
        fields = ["token"]


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favourite
        fields = "__all__"

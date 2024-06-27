import os
import uuid

from django.db import models
from django.utils.text import slugify
from rest_framework.validators import UniqueTogetherValidator


def restaurant_image_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.name)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads/restaurants/", filename)


class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    opening_hours = models.TextField(default=None, blank=True, null=True)
    image = models.ImageField(upload_to=restaurant_image_file_path, blank=True, null=True)

    class Meta:
        validators = [
            UniqueTogetherValidator(
                queryset=Restaurant.objects.all(),
                fields=['list', 'position']
            )
        ]
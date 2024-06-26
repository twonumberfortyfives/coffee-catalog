import os
import uuid

from django.db import models
from django.utils.text import slugify


def restaurant_image_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.name)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads/restaurants/", filename)


class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    opening_hours = models.TextField()
    image = models.ImageField(upload_to=restaurant_image_file_path, blank=True, null=True)


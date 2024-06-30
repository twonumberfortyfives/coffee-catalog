import os
import uuid

from django.db import models
from django.db.models import UniqueConstraint
from django.utils.text import slugify


def restaurant_image_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.name)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads/restaurants/", filename)


class Restaurant(models.Model):
    unique_id = models.CharField(max_length=255, default="Sorry, we dont have address in our database.")
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    opening_hours = models.TextField(default=None, blank=True, null=True)
    images = models.URLField(default=None, blank=True, null=True)

    class Meta:
        constraints = [UniqueConstraint(fields=["name", "address"], name="unique_restaurant")]

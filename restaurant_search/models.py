import os
import uuid

from django.db import models
from django.db.models import UniqueConstraint
from django.utils.text import slugify

from coffee_catalog.settings import AUTH_USER_MODEL


def restaurant_image_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.name)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads/restaurants/", filename)


class Image(models.Model):
    url = models.URLField(max_length=1000)

    def __str__(self):
        return self.url


class Restaurant(models.Model):
    unique_id = models.CharField(max_length=255, default="Sorry, we dont have address in our database.")
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    opening_hours = models.TextField(default=None, blank=True, null=True)
    images = models.ManyToManyField(Image, blank=True)

    class Meta:
        constraints = [UniqueConstraint(fields=["name", "address"], name="unique_restaurant")]

    def __str__(self):
        return f"{self.name} - {self.address}"


class Comment(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField(max_length=1000)

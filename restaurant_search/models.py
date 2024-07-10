from django.db import models
from django.db.models import UniqueConstraint


class Image(models.Model):
    url = models.URLField(max_length=1000)
    restaurant = models.ForeignKey("Restaurant", related_name="images", blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['url', 'restaurant'], name='unique_image_url'),
        ]

    def __str__(self):
        return self.url


class Review(models.Model):
    unique_name = models.CharField(max_length=1000, unique=True, null=True, blank=True)
    restaurant = models.ForeignKey("Restaurant", on_delete=models.CASCADE, related_name="reviews", null=True, blank=True)
    author_name = models.CharField(max_length=255, null=True, blank=True)
    text = models.TextField(max_length=2000, null=True, blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.author_name} - {self.rating} stars"


class Restaurant(models.Model):
    unique_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=1000, null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    google_url = models.URLField(max_length=1000, null=True, blank=True, default=None)
    website_url = models.URLField(max_length=1000, null=True, blank=True)
    total_users_ratings = models.IntegerField(default=0)
    name = models.CharField(max_length=255, null=True, blank=True)
    open_now = models.BooleanField(default=False, null=True, blank=True)
    opening_hours_weekdays = models.JSONField(null=True, blank=True)
    main_photo = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.address}"

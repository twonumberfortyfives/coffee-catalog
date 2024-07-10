# Generated by Django 5.0.6 on 2024-07-08 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("restaurant_search", "0009_alter_restaurant_open_now"),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="image",
            constraint=models.UniqueConstraint(
                fields=("url", "restaurant"), name="unique_image_url"
            ),
        ),
    ]
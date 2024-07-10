# Generated by Django 5.0.6 on 2024-07-08 16:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "restaurant_search",
            "0006_remove_image_restaurant_remove_restaurant_photos_and_more",
        ),
    ]

    operations = [
        migrations.RemoveField(
            model_name="image",
            name="restaurants",
        ),
        migrations.AddField(
            model_name="image",
            name="restaurants",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="images",
                to="restaurant_search.restaurant",
            ),
        ),
    ]

# Generated by Django 5.0.6 on 2024-07-08 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "restaurant_search",
            "0003_remove_restaurant_location_restaurant_latitude_and_more",
        ),
    ]

    operations = [
        migrations.RemoveField(
            model_name="restaurant",
            name="weekdays_opening_hours",
        ),
        migrations.AddField(
            model_name="restaurant",
            name="open_now",
            field=models.BooleanField(default=False),
        ),
    ]

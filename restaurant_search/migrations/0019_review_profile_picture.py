# Generated by Django 5.0.6 on 2024-07-10 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("restaurant_search", "0018_image_contrib_url"),
    ]

    operations = [
        migrations.AddField(
            model_name="review",
            name="profile_picture",
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]

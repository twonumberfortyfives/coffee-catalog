# Generated by Django 5.0.6 on 2024-07-01 13:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0002_favourite"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Favourite",
        ),
    ]

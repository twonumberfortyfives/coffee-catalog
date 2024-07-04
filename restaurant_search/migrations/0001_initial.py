# Generated by Django 5.0.6 on 2024-07-02 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Image",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("url", models.URLField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name="Restaurant",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "unique_id",
                    models.CharField(
                        default="Sorry, we dont have address in our database.",
                        max_length=255,
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("address", models.CharField(max_length=100)),
                (
                    "opening_hours",
                    models.TextField(blank=True, default=None, null=True),
                ),
                (
                    "images",
                    models.ManyToManyField(blank=True, to="restaurant_search.image"),
                ),
            ],
        ),
        migrations.AddConstraint(
            model_name="restaurant",
            constraint=models.UniqueConstraint(
                fields=("name", "address"), name="unique_restaurant"
            ),
        ),
    ]

# Generated by Django 5.0.6 on 2024-07-08 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("restaurant_search", "0012_review_unique_review"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="review",
            name="unique_review",
        ),
        migrations.AddField(
            model_name="review",
            name="unique_name",
            field=models.CharField(default=None, max_length=1000, unique=True),
        ),
    ]
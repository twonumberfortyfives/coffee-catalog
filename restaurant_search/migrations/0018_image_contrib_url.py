# Generated by Django 5.0.6 on 2024-07-10 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("restaurant_search", "0017_alter_review_created_at"),
    ]

    operations = [
        migrations.AddField(
            model_name="image",
            name="contrib_url",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
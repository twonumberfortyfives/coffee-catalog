# Generated by Django 5.0.6 on 2024-07-10 16:49

import django.db.models.deletion
import user.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0006_user_profile_picture"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="profile_picture",
        ),
        migrations.CreateModel(
            name="ProfilePicture",
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
                    "picture",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to=user.models.profile_picture_file_path,
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="profile_picture",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]

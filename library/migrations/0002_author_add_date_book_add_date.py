# Generated by Django 4.2.14 on 2024-07-17 21:26

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("library", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="author",
            name="add_date",
            field=models.DateTimeField(
                auto_now_add=True,
                default=django.utils.timezone.now,
                verbose_name="date added",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="book",
            name="add_date",
            field=models.DateTimeField(
                auto_now_add=True,
                default=django.utils.timezone.now,
                verbose_name="date added",
            ),
            preserve_default=False,
        ),
    ]

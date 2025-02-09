# Generated by Django 5.0.7 on 2024-07-25 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0002_auto_20240725_1507"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="user_age",
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name="movie",
            name="image",
            field=models.ImageField(
                blank=True, null=True, upload_to="static/myapp/img/"
            ),
        ),
    ]

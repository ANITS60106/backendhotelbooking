# Generated by Django 3.0.7 on 2020-09-07 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel_app', '0003_auto_20200906_1309'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='featured',
            field=models.BooleanField(default=False),
        ),
    ]

# Generated by Django 4.2.4 on 2023-08-21 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cryptoApp", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="watchlistmodel",
            name="coinName",
            field=models.CharField(default="Bitcoin", max_length=20),
        ),
    ]

# Generated by Django 4.2.4 on 2023-08-21 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cryptoApp", "0002_watchlistmodel_coinname"),
    ]

    operations = [
        migrations.AlterField(
            model_name="watchlistmodel",
            name="coinName",
            field=models.CharField(max_length=20),
        ),
    ]
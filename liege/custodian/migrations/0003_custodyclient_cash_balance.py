# Generated by Django 3.2.4 on 2021-07-13 21:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custodian', '0002_auto_20210713_1203'),
    ]

    operations = [
        migrations.AddField(
            model_name='custodyclient',
            name='cash_balance',
            field=models.FloatField(default=0, null=True),
        ),
    ]
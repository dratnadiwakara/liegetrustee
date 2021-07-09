# Generated by Django 3.2.4 on 2021-07-05 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custodian', '0005_auto_20210705_1526'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='current_account_number',
            field=models.PositiveIntegerField(blank=True, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='loan_account_number',
            field=models.PositiveIntegerField(blank=True, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='clientbalance',
            name='margin_balance',
            field=models.FloatField(null=True),
        ),
    ]

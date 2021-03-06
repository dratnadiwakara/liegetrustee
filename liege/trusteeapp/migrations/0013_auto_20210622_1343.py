# Generated by Django 3.2.4 on 2021-06-22 18:43

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trusteeapp', '0012_investment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='investment',
            name='fixed_interest_rate',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='investment',
            name='variable_rate_cap',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='investment',
            name='variable_rate_floor',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='investment',
            name='variable_rate_reset_freq',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='investment',
            name='variable_rate_spread',
            field=models.FloatField(blank=True, null=True),
        ),
    ]

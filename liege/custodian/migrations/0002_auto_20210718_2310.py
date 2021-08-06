# Generated by Django 3.2.4 on 2021-07-19 04:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custodian', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Constant',
            fields=[
                ('const_name', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('const_value', models.FloatField()),
                ('last_updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='custodyclient',
            name='margin_interest_rate_type',
            field=models.CharField(choices=[('fixed', 'Fixed'), ('awplr', 'AWPLR+')], default='awplr', max_length=20),
            preserve_default=False,
        ),
    ]
# Generated by Django 3.2.4 on 2021-07-05 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custodian', '0004_auto_20210705_1525'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='cds_no_cbsl',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='client',
            name='cds_no_cse',
            field=models.CharField(max_length=50),
        ),
    ]

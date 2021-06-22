# Generated by Django 3.2.4 on 2021-06-21 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trusteeapp', '0008_securitization_cashflow_checked'),
    ]

    operations = [
        migrations.AlterField(
            model_name='securitization',
            name='audit_report',
            field=models.FileField(blank=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='securitization',
            name='board_resolution',
            field=models.FileField(blank=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='securitization',
            name='td_completedraft',
            field=models.FileField(blank=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='securitization',
            name='td_completesigned',
            field=models.FileField(blank=True, upload_to=''),
        ),
    ]

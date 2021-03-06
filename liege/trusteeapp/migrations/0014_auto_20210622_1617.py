# Generated by Django 3.2.4 on 2021-06-22 21:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trusteeapp', '0013_auto_20210622_1343'),
    ]

    operations = [
        migrations.AddField(
            model_name='securitization',
            name='trust_certificates',
            field=models.FileField(blank=True, upload_to=''),
        ),
        migrations.CreateModel(
            name='Transfer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField()),
                ('transfer_date', models.DateField()),
                ('transfer_complete', models.BooleanField(default=False)),
                ('borrower', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='trusteeapp.borrower')),
                ('investor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='trusteeapp.investor')),
                ('securitization', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='trusteeapp.securitization')),
            ],
        ),
    ]

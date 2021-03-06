# Generated by Django 3.2.4 on 2021-06-21 04:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Borrower',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('borrower_name', models.CharField(max_length=200)),
                ('borrower_address', models.CharField(max_length=300)),
                ('borrower_contact_name', models.CharField(max_length=200)),
                ('borrower_contact_number', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Securitization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('temp_name', models.CharField(max_length=200)),
                ('td_firstdraft', models.FileField(upload_to='documents')),
                ('trust_name', models.CharField(default='', max_length=200)),
                ('trust_bank_account_no', models.CharField(default='', max_length=200)),
                ('trust_bank_account_branch', models.CharField(default='', max_length=200)),
                ('trust_bank_account_bank', models.CharField(default='', max_length=200)),
                ('lawyer_name', models.CharField(max_length=200)),
                ('auditor_name', models.CharField(max_length=200)),
                ('trustee_approved', models.BooleanField(default=False)),
                ('deal_signed', models.BooleanField(default=False)),
                ('borrower', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='trusteeapp.borrower')),
            ],
        ),
        migrations.CreateModel(
            name='Deal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('temp_trust_name', models.CharField(max_length=200)),
                ('requested_date', models.DateTimeField(auto_now_add=True)),
                ('amount_raised', models.IntegerField()),
                ('trust_name', models.CharField(default='', max_length=200)),
                ('trust_bank_account_no', models.CharField(default='', max_length=200)),
                ('trust_bank_account_branch', models.CharField(default='', max_length=200)),
                ('trust_bank_account_bank', models.CharField(default='', max_length=200)),
                ('lawyer_name', models.CharField(max_length=200)),
                ('auditor_name', models.CharField(max_length=200)),
                ('trustee_approved', models.BooleanField(default=False)),
                ('deal_signed', models.BooleanField(default=False)),
                ('td_firstdraft', models.FileField(upload_to='documents')),
                ('borrower', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='trusteeapp.borrower')),
            ],
        ),
    ]

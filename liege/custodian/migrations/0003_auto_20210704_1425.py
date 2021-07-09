# Generated by Django 3.2.4 on 2021-07-04 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custodian', '0002_auto_20210701_2235'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='cds_no_cbsl',
            field=models.CharField(default='CDSno01', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='client',
            name='cds_no_cse',
            field=models.CharField(default='CSE no 1', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='client',
            name='client_birthday',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='client',
            name='current_account_number',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='client',
            name='loan_account_number',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='client',
            name='margin_interest_rate_spread',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='client',
            name='risk_appetite',
            field=models.CharField(choices=[('low', 'Low'), ('moderate', 'Moderate'), ('high', 'High')], default='moderate', max_length=200),
        ),
        migrations.AddField(
            model_name='client',
            name='shariah_compliant',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='client',
            name='target_returns',
            field=models.FloatField(default=0.1),
        ),
        migrations.AlterField(
            model_name='client',
            name='margin_account_balance_date',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='maximum_margin',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='client',
            name='maximum_margin_date',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='payable_amount',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='client',
            name='payable_amount_date',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='receivable_amount',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='client',
            name='receivable_amount_date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
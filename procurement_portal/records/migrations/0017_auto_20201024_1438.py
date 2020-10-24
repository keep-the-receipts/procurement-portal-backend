# Generated by Django 3.1.1 on 2020-10-24 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0016_auto_20201012_0943'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchaserecord',
            name='implementation_status',
            field=models.CharField(blank=True, db_index=True, default='', max_length=500),
        ),
        migrations.AddField(
            model_name='purchaserecord',
            name='reporting_period',
            field=models.CharField(blank=True, db_index=True, default='', max_length=500),
        ),
        migrations.AddField(
            model_name='purchaserecord',
            name='supplier_numbers_other',
            field=models.CharField(blank=True, db_index=True, default='', max_length=500),
        ),
    ]
# Generated by Django 2.2.16 on 2020-09-13 13:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("records", "0004_add_fields_to_searchvectorfield"),
    ]

    operations = [
        migrations.RenameField(
            model_name="purchaserecord",
            old_name="amount_value_rands",
            new_name="amount_value_zar",
        ),
    ]

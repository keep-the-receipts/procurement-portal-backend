# Generated by Django 3.1.1 on 2020-10-24 14:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0017_auto_20201024_1438'),
    ]

    migration = """
        DROP TRIGGER supplier_full_text_content_update ON records_purchaserecord;
        CREATE TRIGGER supplier_full_text_content_update BEFORE INSERT OR UPDATE
        ON records_purchaserecord FOR EACH ROW EXECUTE PROCEDURE
        tsvector_update_trigger(
            supplier_full_text, 'pg_catalog.english',
            supplier_name,
            company_registration_number,
            central_supplier_database_number,
            supplier_numbers_other
         );

        -- Force triggers to run and populate the text_search column.
        UPDATE records_purchaserecord set ID = ID;
    """

    reverse_migration = """
        DROP TRIGGER supplier_full_text_content_update ON records_purchaserecord;
        CREATE TRIGGER supplier_full_text_content_update BEFORE INSERT OR UPDATE
        ON records_purchaserecord FOR EACH ROW EXECUTE PROCEDURE
        tsvector_update_trigger(
            supplier_full_text, 'pg_catalog.english',
            supplier_name, company_registration_number, central_supplier_database_number
         );

        -- Force triggers to run and populate the text_search column.
        UPDATE records_purchaserecord set ID = ID;
    """

    operations = [
        migrations.RunSQL(migration, reverse_migration),
    ]
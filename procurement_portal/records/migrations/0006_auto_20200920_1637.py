# Generated by Django 2.2.16 on 2020-09-20 16:37

import django.contrib.postgres.indexes
import django.contrib.postgres.search
from django.db import migrations, models
import procurement_portal.records.models
import procurement_portal.records.validators


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0005_auto_20200913_1344'),
    ]

    migration = '''
        CREATE TRIGGER supplier_full_text_content_update BEFORE INSERT OR UPDATE
        ON records_purchaserecord FOR EACH ROW EXECUTE PROCEDURE
        tsvector_update_trigger(
            supplier_full_text, 'pg_catalog.english',
            supplier_name
         );
        CREATE TRIGGER directors_full_text_content_update BEFORE INSERT OR UPDATE
        ON records_purchaserecord FOR EACH ROW EXECUTE PROCEDURE
        tsvector_update_trigger(
            directors_full_text, 'pg_catalog.english',
            director_names, director_surnames, director_names_and_surnames
         );
        CREATE TRIGGER description_full_text_content_update BEFORE INSERT OR UPDATE
        ON records_purchaserecord FOR EACH ROW EXECUTE PROCEDURE
        tsvector_update_trigger(
            description_full_text, 'pg_catalog.english',
            items_description, items_quantity
         );
        CREATE TRIGGER procurement_method_full_text_content_update BEFORE INSERT OR UPDATE
        ON records_purchaserecord FOR EACH ROW EXECUTE PROCEDURE
        tsvector_update_trigger(
            procurement_method_full_text, 'pg_catalog.english',
            procurement_method
         );

        -- Force triggers to run and populate the text_search column.
        UPDATE records_purchaserecord set ID = ID;
    '''

    reverse_migration = '''
        DROP TRIGGER supplier_full_text_content_update ON records_purchaserecord;
        DROP TRIGGER directors_full_text_content_update ON records_purchaserecord;
        DROP TRIGGER description_full_text_content_update ON records_purchaserecord;
        DROP TRIGGER procurement_method_full_text_content_update ON records_purchaserecord;
    '''


    operations = [
        migrations.AddField(
            model_name='purchaserecord',
            name='description_full_text',
            field=django.contrib.postgres.search.SearchVectorField(null=True),
        ),
        migrations.AddField(
            model_name='purchaserecord',
            name='directors_full_text',
            field=django.contrib.postgres.search.SearchVectorField(null=True),
        ),
        migrations.AddField(
            model_name='purchaserecord',
            name='procurement_method_full_text',
            field=django.contrib.postgres.search.SearchVectorField(null=True),
        ),
        migrations.AddField(
            model_name='purchaserecord',
            name='supplier_full_text',
            field=django.contrib.postgres.search.SearchVectorField(null=True),
        ),
        migrations.AlterField(
            model_name='datasetversion',
            name='file',
            field=models.FileField(upload_to=procurement_portal.records.models.file_path, validators=[procurement_portal.records.validators.validate_file_extension]),
        ),
        migrations.AddIndex(
            model_name='purchaserecord',
            index=django.contrib.postgres.indexes.GinIndex(fields=['supplier_full_text'], name='records_pur_supplie_ee468a_gin'),
        ),
        migrations.AddIndex(
            model_name='purchaserecord',
            index=django.contrib.postgres.indexes.GinIndex(fields=['directors_full_text'], name='records_pur_directo_b66d88_gin'),
        ),
        migrations.AddIndex(
            model_name='purchaserecord',
            index=django.contrib.postgres.indexes.GinIndex(fields=['description_full_text'], name='records_pur_descrip_35183a_gin'),
        ),
        migrations.AddIndex(
            model_name='purchaserecord',
            index=django.contrib.postgres.indexes.GinIndex(fields=['procurement_method_full_text'], name='records_pur_procure_35237f_gin'),
        ),
        migrations.AddField(
            model_name='purchaserecord',
            name='procurement_method',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.RunSQL(migration, reverse_migration),
    ]
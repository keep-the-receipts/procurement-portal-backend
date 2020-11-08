import os

import tablib
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.safestring import mark_safe
from import_export import resources

from . import models


class PurchaseRecordResource(resources.ModelResource):
    class Meta:
        model = models.PurchaseRecord
        force_init_instance = True
        use_bulk = True
        use_transaction = True


@receiver([post_save], sender=models.DatasetVersion)
def handle_dataset_version_post_save(
    sender, instance, created, raw, using, update_fields, **kwargs
):
    if created:
        ext = os.path.splitext(instance.file.name)[1][1:]  # [0] returns path+filename
        dataset = tablib.Dataset().load(instance.file.open("r"), ext)
        dataset.append_col([instance.pk] * len(dataset), header="dataset_version")
        resource = PurchaseRecordResource()
        result = resource.import_data(dataset)

        if result.has_errors():
            instance.import_report = build_error_message(result)
        else:
            instance.imported = True
            instance.import_report = "OK"

        if instance.imported:
            instance.dataset.current_version = instance

        instance.dataset.save()


def build_error_message(result):
    message = "Parsing error(s)<br/>Invalid rows:<br/>"
    for invalid_row in result.row_errors():
        errors_info = [(e.error, e.row) for e in invalid_row[1]]
        errors = [str(e[0])[2:-2] for e in errors_info]
        row = ",".join([str(e) for e in errors_info[0][1].values()])
        message += f"Row: {invalid_row[0]}<br/>errors: {errors}<br/>values: {row} <br/>"

    return mark_safe(message[:-5]).strip()

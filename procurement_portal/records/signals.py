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
            instance._error_message = build_error_message(result)
            return

        counts = instance._count_purchase_record_fields()
        missing_fields = [
            field
            for field in {"buyer_name", "supplier_name", "order_amount_zar"}
            if counts[field] == 0
        ]
        if missing_fields:
            raise ValidationError(
                "Missing field(s): {}".format(", ".join(missing_fields))
            )

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

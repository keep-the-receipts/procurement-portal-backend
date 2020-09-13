from . import models
from django.db.models.signals import post_save
from django.dispatch import receiver
import tablib
from import_export import resources
import os


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
        dataset.append_col([instance.pk]*len(dataset), header='dataset_version')
        resource = PurchaseRecordResource()
        resource.import_data(dataset, raise_errors=True)

        instance.dataset.current_version = instance
        instance.dataset.save()

from procurement_portal import models
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver([post_save], sender=models.DatasetVersion)
def handle_irm_snapshot_post_save(
    sender, instance, created, raw, using, update_fields, **kwargs
):
    if created:
        instance.dataset.current_version = instance

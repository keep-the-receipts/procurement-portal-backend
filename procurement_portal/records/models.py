from django.db import models
from datetime import datetime
from django_extensions.db.models import TimeStampedModel
from django.contrib.postgres.search import SearchVectorField
from django.contrib.postgres.indexes import GinIndex


## FIXME remove when redoing migrations
class UpdateTimestampsMixin:
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Repository(TimeStampedModel):
    name = models.CharField(max_length=250)
    description = models.TextField()

    def __str__(self):
        return self.name


class Dataset(TimeStampedModel):
    repository = models.ForeignKey("Repository", on_delete=models.CASCADE)
    current_version = models.ForeignKey(
        "DatasetVersion",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="+",
    )
    name = models.CharField(max_length=250)
    description = models.TextField()
    provenance = models.TextField()
    online_source_url = models.URLField(max_length=300, null=True, blank=True)
    trusted_archive_url = models.URLField(max_length=300, null=True, blank=True)
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({ self.repository.name })"


def file_path(instance, filename):
    extension = filename.split(".")[-1]
    return (
        f"dataset-uploads/"
        f"{instance.dataset.name}-{datetime.now().isoformat()}.{extension}"
    )


class DatasetVersion(TimeStampedModel):
    dataset = models.ForeignKey("Dataset", on_delete=models.CASCADE)
    description = models.TextField()
    file = models.FileField(upload_to=file_path)

    def __str__(self):
        return f"{self.dataset.name} ({ self.created })"


class PurchaseRecord(TimeStampedModel):
    dataset_version = models.ForeignKey("DatasetVersion", on_delete=models.CASCADE)
    buyer_name = models.CharField(max_length=500)
    supplier_name = models.CharField(max_length=500)
    amount_value_zar = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    items_description = models.TextField(null=True, blank=True)
    items_quantity = models.TextField(null=True, blank=True)
    director_names = models.TextField(null=True, blank=True)
    director_surnames = models.TextField(null=True, blank=True)
    director_names_and_surnames = models.TextField(null=True, blank=True)
    company_registration_number = models.CharField(max_length=500, null=True, blank=True)
    central_supplier_database_number = models.CharField(max_length=500, null=True, blank=True)
    implementation_location = models.CharField(max_length=500, null=True, blank=True)
    implementation_location_province = models.CharField(max_length=500, null=True, blank=True)
    implementation_location_district_municipality = models.CharField(max_length=500, null=True, blank=True)
    implementation_location_local_municipality = models.CharField(max_length=500, null=True, blank=True)
    implementation_location_facility = models.CharField(max_length=500, null=True, blank=True)
    implementation_location_other = models.CharField(max_length=500, null=True, blank=True)

    full_text_search = SearchVectorField(null=True)

    class Meta:
        indexes = [GinIndex(fields=["full_text_search"])]

    def __str__(self):
        return self.supplier_name

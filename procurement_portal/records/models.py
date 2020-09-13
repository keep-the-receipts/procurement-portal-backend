from django.db import models
from datetime import datetime


class UpdateTimestampsMixin:
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Repository(models.Model, UpdateTimestampsMixin):
    name = models.CharField(max_length=250)
    description = models.TextField()

    def __str__(self):
        return self.name


class Dataset(models.Model, UpdateTimestampsMixin):
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


class DatasetVersion(models.Model, UpdateTimestampsMixin):
    dataset = models.ForeignKey("Dataset", on_delete=models.CASCADE)
    description = models.TextField()
    file = models.FileField(upload_to=file_path)

    def __str__(self):
        return f"{self.dataset.name} ({ self.updated })"


class PurchaseRecord(models.Model, UpdateTimestampsMixin):
    dataset_version = models.ForeignKey("DatasetVersion", on_delete=models.CASCADE)
    supplier_name = models.CharField(max_length=500)
    amount = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.supplier_name

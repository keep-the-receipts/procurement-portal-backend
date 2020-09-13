from rest_framework import serializers

from . import models


class PurchaseRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PurchaseRecord
        fields = [
            "dataset_version",
            "supplier_name",
            "amount",
        ]

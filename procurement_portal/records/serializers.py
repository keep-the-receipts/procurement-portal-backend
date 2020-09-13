from rest_framework import serializers

from . import models


class PurchaseRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PurchaseRecord
        fields = [
            "dataset_version",
            "supplier_name",
            "amount_value_zar",
            "supplier_name",
            "buyer_name",
            "central_supplier_database_number",
            "company_registration_number",
            "director_names",
            "director_names_and_surnames",
            "director_surnames",
            "implementation_location",
            "implementation_location_district_municipality",
            "implementation_location_facility",
            "implementation_location_local_municipality",
            "implementation_location_other",
            "implementation_location_province",
            "items_description",
            "items_quantity",
        ]

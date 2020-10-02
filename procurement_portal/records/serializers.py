from rest_framework import serializers

from . import models


class PurchaseRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PurchaseRecord
        fields = [
            "supplier_name",
            "order_amount_zar",
            "invoice_amount_zar",
            "payment_amount_zar",
            "cost_per_unit_zar",
            "supplier_name",
            "buyer_name",
            "central_supplier_database_number",
            "company_registration_number",
            "director_names",
            "director_names_and_surnames",
            "director_surnames",
            "implementation_location_district_municipality",
            "implementation_location_facility",
            "implementation_location_local_municipality",
            "implementation_location_other",
            "implementation_location_province",
            "items_description",
            "items_quantity",
            "items_unit",
            "procurement_method",
            "state_employee",
            "award_date",
            "invoice_date",
            "invoice_receipt_date",
            "payment_date",
            "order_number",
            "invoice_number",
            "payment_number",
            "payment_period",
            "bbbee_status",
        ]


class DatasetVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DatasetVersion
        fields = [
            "id",
            "description",
            "file",
            "dataset",
            "column_stats",
            "matched_columns",
            "missing_columns",
            "matched_columns_count",
            "missing_columns_count",
            "total_columns_count",
        ]


class DatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Dataset
        fields = "__all__"

    current_version = DatasetVersionSerializer()

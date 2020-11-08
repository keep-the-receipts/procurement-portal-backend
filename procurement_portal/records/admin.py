from django.contrib import admin

from . import models


class DatasetVersionInline(admin.StackedInline):
    model = models.DatasetVersion

    fields = [
        "dataset",
        "description",
        "file",
        "imported",
        "import_report",
        (
            "record_count",
            "matched_columns_count",
            "missing_columns_count",
            "total_columns_count",
            "column_stats_html",
        ),
    ]

    readonly_fields = [
        "imported",
        "import_report",
        "record_count",
        "matched_columns_count",
        "missing_columns_count",
        "total_columns_count",
        "column_stats_html",
    ]

    # Always show exactly one new inline form.
    def get_max_num(self, request, obj=None, **kwargs):
        if obj:
            return obj.versions.count() + 1
        else:
            return 1


class DatasetAdmin(admin.ModelAdmin):
    inlines = [
        DatasetVersionInline,
    ]

    list_display = [
        "name",
        "current_version_created_date",
        "latest_version_created_date",
        "latest_version_is_imported",
    ]

    def current_version_created_date(self, obj):
        if obj and obj.current_version:
            return obj.current_version.created

    def latest_version_created_date(self, obj):
        if obj and obj.latest_version:
            return obj.latest_version.created

    def latest_version_is_imported(self, obj):
        if obj and obj.latest_version:
            return obj.latest_version.imported

    latest_version_is_imported.boolean = True


admin.site.register(models.Repository)
admin.site.register(models.Dataset, DatasetAdmin)
admin.site.register(models.PurchaseRecord)

from django.contrib import admin

from . import models


class DatasetVersionInline(admin.TabularInline):
    model = models.DatasetVersion

    fields = [
        "dataset",
        "description",
        "file",
        "imported",
        "import_report",
        "record_count",
        "matched_columns_count",
        "missing_columns_count",
        "total_columns_count",
        "column_stats_html",
    ]

    readonly_fields = [
        "file",
        "imported",
        "import_report",
    ]

    ordering = ("-pk",)

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
        "current_version"
    ]


admin.site.register(models.Repository)
admin.site.register(models.Dataset, DatasetAdmin)
admin.site.register(models.PurchaseRecord)

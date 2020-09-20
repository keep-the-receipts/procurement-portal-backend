from django.contrib import admin
from . import models


class DatasetVersionInline(admin.TabularInline):
    model = models.DatasetVersion


class DatasetAdmin(admin.ModelAdmin):
    inlines = [
        DatasetVersionInline,
    ]


admin.site.register(models.Repository)
admin.site.register(models.Dataset, DatasetAdmin)
admin.site.register(models.PurchaseRecord)

class DatasetVersionAdmin(admin.ModelAdmin):
    readonly_fields = [
        'record_count',
        'matched_columns_count', 'missing_columns_count', 'total_columns_count',
        'column_stats_html',
    ]
    fields = [
        'dataset', 'description', 'file',
        'record_count',
        'matched_columns_count', 'missing_columns_count', 'total_columns_count',
        'column_stats_html',
    ]
    list_display = [
        'dataset', 'description', 'file',
        'record_count', 'matched_columns_count', 'missing_columns_count', 'total_columns_count'
    ]

admin.site.register(models.DatasetVersion, DatasetVersionAdmin)

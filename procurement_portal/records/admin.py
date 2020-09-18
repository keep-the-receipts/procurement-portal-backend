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
admin.site.register(models.DatasetVersion)
admin.site.register(models.PurchaseRecord)

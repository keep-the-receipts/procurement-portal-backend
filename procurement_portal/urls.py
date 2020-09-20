from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from .records import views as records_views

from . import views


urlpatterns = [
    path("", views.Index.as_view(), name="index"),
    path(
        "records",
        include("procurement_portal.records.urls"),
    ),
    path("admin/", admin.site.urls),
    path(
        "api/purchase_records/",
        records_views.PurchaseRecordJSONListView.as_view(),
        name="purchase-records-api",
    ),
    path(
        "records/purchase_records.xlsx",
        records_views.PurchaseRecordXLSXListView.as_view(),
        name="purchase-records-xlsx",
    ),
    path("api/datasets/", records_views.DatasetView.as_view()),
    path("api/dataset_versions/", records_views.DatasetVersionView.as_view()),
]

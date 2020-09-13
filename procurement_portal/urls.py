from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from .records import views as records_views

from . import views

api_router = routers.DefaultRouter()
api_router.register(r"purchase_records", records_views.PurchaseRecordViewSet)

urlpatterns = [
    path("", views.Index.as_view(), name="index"),
    path("records", include("procurement_portal.records.urls"),),
    path("admin/", admin.site.urls),
    path("api/", include(api_router.urls)),
]

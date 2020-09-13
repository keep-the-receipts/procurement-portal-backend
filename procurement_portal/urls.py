from django.contrib import admin
from django.urls import include, path

from . import views


urlpatterns = [
    path("", views.Index.as_view(), name="index"),
    path("records", include("procurement_portal.records.urls"),),
    path("admin/", admin.site.urls),
]

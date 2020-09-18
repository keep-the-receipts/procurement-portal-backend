from django.views import generic
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import PurchaseRecordSerializer
from . import models
from .filters import FullTextSearchFilter
from django.db.models import F


class Index(generic.TemplateView):
    template_name = "records/index.html"


class PurchaseRecordViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.PurchaseRecord.objects.filter(dataset_version=F('dataset_version__dataset__current_version'))
    serializer_class = PurchaseRecordSerializer
    filter_backends = [DjangoFilterBackend, FullTextSearchFilter]

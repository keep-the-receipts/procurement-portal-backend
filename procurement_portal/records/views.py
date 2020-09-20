from django.views import generic
from rest_framework import generics as drf_generics
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import DatasetSerializer, DatasetVersionSerializer, PurchaseRecordSerializer
from . import models
from .filters import FullTextSearchFilter, FacetFieldFilter
from django.db.models import F
from drf_renderer_xlsx.mixins import XLSXFileMixin
from drf_renderer_xlsx.renderers import XLSXRenderer
from django.urls import reverse


class Index(generic.TemplateView):
    template_name = "records/index.html"


class BasePurchaseRecordListView(drf_generics.ListAPIView):
    queryset = models.PurchaseRecord.objects.filter(
        dataset_version=F("dataset_version__dataset__current_version")
    )
    serializer_class = PurchaseRecordSerializer
    filter_backends = [FullTextSearchFilter, FacetFieldFilter]
    facet_filter_fields = [
        "buyer_name",
        "implementation_location_province",
        "implementation_location_district_municipality",
        "implementation_location_local_municipality",
        "implementation_location_facility",
        "implementation_location_other",
        "dataset_version__dataset__name",
        "dataset_version__dataset__repository__name",
    ]
    full_text_filter_fields = [
        "supplier_full_text",
        "directors_full_text",
        "description_full_text",
        "procurement_method_full_text",
    ]


class PurchaseRecordJSONListView(BasePurchaseRecordListView):
    def __init__(self, *args, **kwargs):
        super(BasePurchaseRecordListView, self).__init__(*args, **kwargs)
        self.facets = {}

    def list(self, request, *args, **kwargs):
        result = super(BasePurchaseRecordListView, self).list(request, *args, **kwargs)
        result.data["meta"] = {
            "facets": self.facets,
            "xlsx_url": self._get_xlsx_url(request),
        }
        return result

    def _get_xlsx_url(self, request):
        querydict = request.GET.copy()

        # The XLSXListview shouldn't pay attention to pagination info, but
        # it's less confusing if they're not in the URL in the first place.
        if "count" in querydict:
            del querydict["count"]
        if "limit" in querydict:
            del querydict["limit"]

        return request.build_absolute_uri(
            f"{reverse('purchase-records-xlsx')}?{querydict.urlencode()}"
        )


class PurchaseRecordXLSXListView(XLSXFileMixin, BasePurchaseRecordListView):
    renderer_classes = (XLSXRenderer,)
    pagination_class = None
    filename = 'purchase-records.xlsx'


class DatasetVersionView(drf_generics.ListAPIView):
    queryset = models.DatasetVersion.objects.filter(pk=F("dataset__current_version"))
    serializer_class = DatasetVersionSerializer
    # filter_backends = [DjangoFilterBackend, FullTextSearchFilter]


class DatasetView(drf_generics.ListAPIView):
    queryset = models.Dataset.objects.all()
    serializer_class = DatasetSerializer
    # filter_backends = [DjangoFilterBackend, FullTextSearchFilter]

from django.db.models import F
from django.http import StreamingHttpResponse
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.cache import cache_page
from django_filters.rest_framework import DjangoFilterBackend
from drf_renderer_xlsx.mixins import XLSXFileMixin
from rest_framework import generics as drf_generics
import xlsx_streaming

from . import models
from .filters import FacetFieldFilter, FullTextSearchFilter
from .serializers import (
    DatasetSerializer,
    DatasetVersionSerializer,
    PurchaseRecordSerializer,
)


PURCHASE_RECORD_XLSX_FIELDS = [
    "supplier_name",
    "order_amount_zar",
    "invoice_amount_zar",
    "payment_amount_zar",
    "cost_per_unit_zar",
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
    "dataset_version__dataset__name",
    "dataset_version__dataset__repository__name",
    "dataset_version__created",
    "dataset_version__modified",
    "dataset_version__description",
    "dataset_version__file"
]


class Index(generic.TemplateView):
    template_name = "records/index.html"


class BasePurchaseRecordListView(drf_generics.ListAPIView):
    queryset = (
        models.PurchaseRecord.objects.filter(
            dataset_version=F("dataset_version__dataset__current_version")
        )
        .order_by(F("order_amount_zar").desc(nulls_last=True))
        .prefetch_related("dataset_version__dataset__repository")
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

    @method_decorator(cache_page(60 * 2))  # cache 2 minutes
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
    pagination_class = None
    template_filename = "template.xlsx"
    filename = "purchase-records.xlsx"

    @method_decorator(cache_page(60 * 2))  # cache 2 minutes
    def list(self, request, *args, **kwargs):

        with open(self.template_filename, "rb") as template:
            stream = xlsx_streaming.stream_queryset_as_xlsx(
                self.filter_queryset(self.get_queryset()).values_list(
                    *PURCHASE_RECORD_XLSX_FIELDS
                ),
                xlsx_template=template,
                batch_size=50,
            )
        response = StreamingHttpResponse(
            stream,
            content_type="application/vnd.xlsxformats-officedocument.spreadsheetml.sheet",
        )
        response["Content-Disposition"] = f"attachment; filename={self.filename}"
        return response


class DatasetVersionView(drf_generics.ListAPIView):
    queryset = models.DatasetVersion.objects.filter(pk=F("dataset__current_version"))
    serializer_class = DatasetVersionSerializer
    # filter_backends = [DjangoFilterBackend, FullTextSearchFilter]


class DatasetView(drf_generics.ListAPIView):
    queryset = models.Dataset.objects.all()
    serializer_class = DatasetSerializer
    # filter_backends = [DjangoFilterBackend, FullTextSearchFilter]

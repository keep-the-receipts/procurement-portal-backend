from django.contrib.postgres.search import SearchQuery, SearchVector
from rest_framework.filters import BaseFilterBackend
from django import forms
from django.utils.safestring import mark_safe
import re
from django.db.models import Count, F


PHRASE_RE = re.compile(r'"([^"]*)("|$)')


class FacetFieldFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        field_set = set(view.facet_filter_fields)

        filters = {}
        for field in field_set:
            values = request.GET.getlist(field, None)
            if values:
                filters[field] = values
        print(filters)

        for field in field_set:
            other_filters = filters.copy()
            if field in other_filters:
                del other_filters[field]

            other_filtered_qs = queryset
            for field, values in other_filters.items():
                other_filtered_qs = other_filtered_qs.filter(**{f"{field}__in": values})

            view.facets[field] = (
                queryset.values(label=F(field))
                .annotate(count=Count("*"))
                .order_by("-count", "label")
                .all()
            )

        for field, values in filters.items():
            queryset = queryset.filter(**{f"{field}__in": values})

        return queryset

    def to_html(self, request, queryset, view):
        fields = FullTextSearchForm().as_p()
        return mark_safe(f'<form action="" method="get">{ fields }</form>')


class FullTextSearchFilter(BaseFilterBackend):
    """
    Filter on phrase provided by
    """

    def filter_queryset(self, request, queryset, view):

        query = request.query_params.get("basic_web_search", None)

        if query:

            phrases = [p[0].strip() for p in PHRASE_RE.findall(query)]
            phrases = [p for p in phrases if p]
            terms = PHRASE_RE.sub("", query).strip()

            if terms:
                compound_statement = SearchQuery(terms)

            if phrases:
                if terms:
                    compound_statement = compound_statement & SearchQuery(
                        phrases[0], search_type="phrase"
                    )
                else:
                    compound_statement = SearchQuery(phrases[0], search_type="phrase")

                for phrase in phrases[1:]:
                    compound_statement = compound_statement & SearchQuery(
                        phrase, search_type="phrase"
                    )
            if terms or phrases:
                print(compound_statement)

                queryset = queryset.filter(full_text_search=compound_statement)

        return queryset

    def to_html(self, request, queryset, view):
        fields = FullTextSearchForm().as_p()
        return mark_safe(f'<form action="" method="get">{ fields }</form>')


class FullTextSearchForm(forms.Form):
    basic_web_search = forms.CharField(label="Full text search")

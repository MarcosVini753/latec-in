from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from django.db.models import Q
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter

from apps.common.models import EditorialStatus


ECOSYSTEM_UNIT_PARAMETER = OpenApiParameter(
    "unit",
    OpenApiTypes.STR,
    description=(
        "Slug da unidade. Inclui conteúdo próprio e conteúdo de filhas diretas "
        "com opt-in no ecossistema; não agrega netas."
    ),
)


class PublicReadOnlyModelViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field = "slug"
    search_fields = ("title", "name", "full_name")

    def get_queryset(self):
        queryset = super().get_queryset()
        model_fields = {field.name: field for field in queryset.model._meta.fields}
        many_to_many_fields = {field.name for field in queryset.model._meta.many_to_many}

        if "is_active" in model_fields:
            queryset = queryset.filter(is_active=True)
        if "editorial_status" in model_fields:
            queryset = queryset.filter(editorial_status=EditorialStatus.PUBLISHED)

        unit = self.request.query_params.get("unit")
        if unit and "unit" in model_fields:
            unit_scope = Q(unit__slug=unit)
            if "include_in_parent_ecosystem" in model_fields:
                unit_scope |= Q(
                    unit__parent__slug=unit,
                    include_in_parent_ecosystem=True,
                )
            queryset = queryset.filter(unit_scope)
        elif unit and "units" in many_to_many_fields:
            queryset = queryset.filter(units__slug=unit).distinct()

        axis = self.request.query_params.get("axis")
        if axis and "axis" in model_fields:
            queryset = queryset.filter(axis__slug=axis)

        category = self.request.query_params.get("category")
        if category and "category" in model_fields:
            queryset = queryset.filter(category__slug=category)

        status = self.request.query_params.get("status")
        if status and "status" in model_fields:
            queryset = queryset.filter(status__slug=status)

        year = self.request.query_params.get("year")
        year_lookup = None
        if "year" in model_fields:
            year_lookup = "year"
        elif "start_date" in model_fields:
            year_lookup = "start_date__year"
        elif "publication_date" in model_fields:
            year_lookup = "publication_date__year"
        elif "published_at" in model_fields:
            year_lookup = "published_at__year"

        if year is not None and year_lookup:
            try:
                year_value = int(year)
            except (TypeError, ValueError):
                raise ValidationError({"year": "Informe um ano inteiro válido."})
            if not 1 <= year_value <= 9999:
                raise ValidationError({"year": "Informe um ano entre 1 e 9999."})
            queryset = queryset.filter(**{year_lookup: year_value})

        search = self.request.query_params.get("search")
        if search:
            search_query = None
            for field_name in self.search_fields:
                if field_name in model_fields:
                    condition = {f"{field_name}__icontains": search}
                    search_query = queryset.filter(**condition) if search_query is None else search_query | queryset.filter(**condition)
            if search_query is not None:
                queryset = search_query.distinct()

        return queryset

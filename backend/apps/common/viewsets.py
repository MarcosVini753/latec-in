from rest_framework import viewsets
from rest_framework.exceptions import ValidationError

from apps.common.models import EditorialStatus


class PublicReadOnlyModelViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field = "slug"
    search_fields = ("title", "name", "full_name")

    def get_queryset(self):
        queryset = super().get_queryset()
        model_fields = {field.name: field for field in queryset.model._meta.fields}
        many_to_many_fields = {field.name for field in queryset.model._meta.many_to_many}

        if "is_active" in model_fields:
            queryset = queryset.filter(is_active=True)
        if "is_published" in model_fields:
            queryset = queryset.filter(is_published=True)
        if "editorial_status" in model_fields:
            queryset = queryset.filter(editorial_status=EditorialStatus.PUBLISHED)
        if self._is_editorial_status_field(model_fields.get("status")):
            queryset = queryset.filter(status=EditorialStatus.PUBLISHED)

        unit = self.request.query_params.get("unit")
        if unit and "unit" in model_fields:
            queryset = queryset.filter(unit__slug=unit)
        elif unit and "units" in many_to_many_fields:
            queryset = queryset.filter(units__slug=unit).distinct()

        axis = self.request.query_params.get("axis")
        if axis and "axis" in model_fields:
            queryset = queryset.filter(axis__slug=axis)

        category = self.request.query_params.get("category")
        if category and "category" in model_fields:
            queryset = queryset.filter(category__slug=category)

        status = self.request.query_params.get("status")
        if status and "status" in model_fields and not self._is_editorial_status_field(model_fields["status"]):
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

        featured = self.request.query_params.get("featured")
        if featured in {"true", "1"} and "is_featured" in model_fields:
            queryset = queryset.filter(is_featured=True)
        elif featured in {"false", "0"} and "is_featured" in model_fields:
            queryset = queryset.filter(is_featured=False)
        elif featured is not None and "is_featured" in model_fields:
            raise ValidationError({"featured": "Use true, false, 1 ou 0."})

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

    def _is_editorial_status_field(self, field):
        if not field or not field.choices:
            return False
        choice_values = {value for value, _label in field.choices}
        return EditorialStatus.PUBLISHED in choice_values and EditorialStatus.ARCHIVED in choice_values

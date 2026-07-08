from rest_framework import viewsets

from apps.common.models import EditorialStatus


class PublicReadOnlyModelViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field = "slug"
    search_fields = ("title", "name", "full_name")

    def get_queryset(self):
        queryset = super().get_queryset()
        model_fields = {field.name: field for field in queryset.model._meta.fields}

        if "is_active" in model_fields:
            queryset = queryset.filter(is_active=True)
        if "is_published" in model_fields:
            queryset = queryset.filter(is_published=True)
        if "editorial_status" in model_fields:
            queryset = queryset.filter(editorial_status=EditorialStatus.PUBLISHED)
        if "status" in model_fields and model_fields["status"].choices:
            queryset = queryset.filter(status=EditorialStatus.PUBLISHED)

        axis = self.request.query_params.get("axis")
        if axis and "axis" in model_fields:
            queryset = queryset.filter(axis__slug=axis)

        category = self.request.query_params.get("category")
        if category and "category" in model_fields:
            queryset = queryset.filter(category__slug=category)

        year = self.request.query_params.get("year")
        if year and "year" in model_fields:
            queryset = queryset.filter(year=year)

        featured = self.request.query_params.get("featured")
        if featured in {"true", "1"} and "is_featured" in model_fields:
            queryset = queryset.filter(is_featured=True)

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

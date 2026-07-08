from django.utils import timezone

from apps.common.models import EditorialStatus


def _editorial_status_field(model):
    field_names = {field.name for field in model._meta.fields}
    if "editorial_status" in field_names:
        return "editorial_status"
    if "status" in field_names:
        return "status"
    return None


def mark_as_published(modeladmin, request, queryset):
    status_field = _editorial_status_field(queryset.model)
    updates = {}
    if status_field:
        updates[status_field] = EditorialStatus.PUBLISHED
    if any(field.name == "is_published" for field in queryset.model._meta.fields):
        updates["is_published"] = True
    if any(field.name == "published_at" for field in queryset.model._meta.fields):
        updates["published_at"] = timezone.now()
    if updates:
        queryset.update(**updates)


mark_as_published.short_description = "Publicar selecionados"


def mark_as_in_review(modeladmin, request, queryset):
    status_field = _editorial_status_field(queryset.model)
    updates = {}
    if status_field:
        updates[status_field] = EditorialStatus.IN_REVIEW
    if any(field.name == "is_published" for field in queryset.model._meta.fields):
        updates["is_published"] = False
    if updates:
        queryset.update(**updates)


mark_as_in_review.short_description = "Enviar selecionados para revisão"


def mark_as_archived(modeladmin, request, queryset):
    status_field = _editorial_status_field(queryset.model)
    updates = {}
    if status_field:
        updates[status_field] = EditorialStatus.ARCHIVED
    if any(field.name == "is_published" for field in queryset.model._meta.fields):
        updates["is_published"] = False
    if updates:
        queryset.update(**updates)


mark_as_archived.short_description = "Arquivar selecionados"


EDITORIAL_ADMIN_ACTIONS = (mark_as_published, mark_as_in_review, mark_as_archived)

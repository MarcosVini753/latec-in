from django.utils import timezone
from django.db.models import Q

from apps.common.models import EditorialStatus


def _editorial_status_field(model):
    field_names = {field.name for field in model._meta.fields}
    return "editorial_status" if "editorial_status" in field_names else None


def _authorized_queryset(modeladmin, request, queryset, *, publication=False):
    if not modeladmin.has_change_permission(request):
        return queryset.none()
    if publication and not getattr(modeladmin, "can_publish", lambda _request: False)(request):
        return queryset.none()
    allowed = modeladmin.get_queryset(request).filter(pk__in=queryset.values("pk"))
    if not publication and not getattr(modeladmin, "can_publish", lambda _request: False)(request):
        published = Q()
        status_field = _editorial_status_field(queryset.model)
        if status_field:
            published |= Q(
                **{f"{status_field}__in": (EditorialStatus.PUBLISHED, EditorialStatus.ARCHIVED)}
            )
        elif any(field.name == "is_published" for field in queryset.model._meta.fields):
            published |= Q(is_published=True)
        if published:
            allowed = allowed.exclude(published)
    return allowed


def mark_as_published(modeladmin, request, queryset):
    queryset = _authorized_queryset(modeladmin, request, queryset, publication=True)
    status_field = _editorial_status_field(queryset.model)
    updates = {}
    if status_field:
        updates[status_field] = EditorialStatus.PUBLISHED
    elif any(field.name == "is_published" for field in queryset.model._meta.fields):
        updates["is_published"] = True
    if any(field.name == "published_at" for field in queryset.model._meta.fields):
        updates["published_at"] = timezone.now()
    if updates:
        queryset.update(**updates)


mark_as_published.short_description = "Publicar selecionados"


def mark_as_in_review(modeladmin, request, queryset):
    queryset = _authorized_queryset(modeladmin, request, queryset)
    status_field = _editorial_status_field(queryset.model)
    updates = {}
    if status_field:
        updates[status_field] = EditorialStatus.IN_REVIEW
    elif any(field.name == "is_published" for field in queryset.model._meta.fields):
        updates["is_published"] = False
    if updates:
        queryset.update(**updates)


mark_as_in_review.short_description = "Enviar selecionados para revisão"


def mark_as_archived(modeladmin, request, queryset):
    queryset = _authorized_queryset(modeladmin, request, queryset, publication=True)
    status_field = _editorial_status_field(queryset.model)
    updates = {}
    if status_field:
        updates[status_field] = EditorialStatus.ARCHIVED
    elif any(field.name == "is_published" for field in queryset.model._meta.fields):
        updates["is_published"] = False
    if updates:
        queryset.update(**updates)


mark_as_archived.short_description = "Arquivar selecionados"


EDITORIAL_ADMIN_ACTIONS = (mark_as_published, mark_as_in_review, mark_as_archived)

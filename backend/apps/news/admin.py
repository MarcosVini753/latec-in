from django.contrib import admin

from apps.common.admin_actions import EDITORIAL_ADMIN_ACTIONS
from apps.common.admin_scoping import UnitScopedAdminMixin
from apps.news.models import Post


@admin.register(Post)
class PostAdmin(UnitScopedAdminMixin, admin.ModelAdmin):
    axis_lookup = "axis"
    list_display = ("title", "unit", "axis", "editorial_status", "include_in_parent_ecosystem", "published_at")
    list_filter = ("unit", "editorial_status", "axis", "include_in_parent_ecosystem")
    search_fields = ("title", "summary", "content", "unit__name", "unit__acronym")
    prepopulated_fields = {"slug": ("title",)}
    autocomplete_fields = ("unit", "axis")
    list_select_related = ("unit", "axis")
    actions = EDITORIAL_ADMIN_ACTIONS
    fieldsets = (
        ("Identificação", {"fields": ("unit", "title", "slug", "axis")}),
        ("Conteúdo", {"fields": ("summary", "content", "cover_image")}),
        ("Publicação", {"fields": ("editorial_status", "published_at", "include_in_parent_ecosystem")}),
    )

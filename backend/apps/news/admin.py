from django.contrib import admin

from apps.common.admin_actions import EDITORIAL_ADMIN_ACTIONS
from apps.common.admin_scoping import ReferenceAdminMixin, UnitScopedAdminMixin
from apps.news.models import Post, PostCategory, Tag


@admin.register(PostCategory)
class PostCategoryAdmin(ReferenceAdminMixin, admin.ModelAdmin):
    management_access = "lab"
    list_display = ("name", "slug", "is_active", "display_order")
    list_filter = ("is_active",)
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Tag)
class TagAdmin(ReferenceAdminMixin, admin.ModelAdmin):
    management_access = "lab"
    list_display = ("name", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Post)
class PostAdmin(UnitScopedAdminMixin, admin.ModelAdmin):
    axis_lookup = "axis"
    list_display = ("title", "unit", "category", "axis", "status", "is_published", "is_featured", "published_at")
    list_filter = ("unit", "category", "status", "axis", "is_published", "is_featured")
    search_fields = ("title", "summary", "content", "unit__name", "unit__acronym")
    prepopulated_fields = {"slug": ("title",)}
    autocomplete_fields = ("unit", "axis", "category", "authors", "tags")
    list_select_related = ("unit", "category", "axis")
    actions = EDITORIAL_ADMIN_ACTIONS
    fieldsets = (
        ("Identificação", {"fields": ("unit", "title", "slug", "axis", "category", "tags", "authors")}),
        ("Conteúdo", {"fields": ("summary", "content", "cover_image")}),
        ("Publicação", {"fields": ("status", "is_published", "published_at", "is_featured", "display_order")}),
    )

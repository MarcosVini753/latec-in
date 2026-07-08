from django.contrib import admin

from apps.portfolio.models import Project, ProjectCategory, ProjectLink, ProjectResult, ProjectStatus, ProjectTeamMember


@admin.register(ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "is_active", "display_order")
    list_filter = ("is_active",)
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(ProjectStatus)
class ProjectStatusAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "display_order")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


class ProjectTeamMemberInline(admin.TabularInline):
    model = ProjectTeamMember
    extra = 0
    autocomplete_fields = ("person",)


class ProjectResultInline(admin.TabularInline):
    model = ProjectResult
    extra = 0


class ProjectLinkInline(admin.TabularInline):
    model = ProjectLink
    extra = 0


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "axis", "category", "status", "editorial_status", "is_published", "is_featured", "year")
    list_filter = ("axis", "category", "status", "editorial_status", "is_published", "is_featured", "year")
    search_fields = ("title", "summary", "area", "problem", "solution")
    prepopulated_fields = {"slug": ("title",)}
    autocomplete_fields = ("axis", "category", "status")
    inlines = (ProjectTeamMemberInline, ProjectResultInline, ProjectLinkInline)


@admin.register(ProjectTeamMember)
class ProjectTeamMemberAdmin(admin.ModelAdmin):
    list_display = ("project", "person", "role", "is_lead", "display_order")
    list_filter = ("is_lead", "role")
    search_fields = ("project__title", "person__full_name", "role")
    autocomplete_fields = ("project", "person")


@admin.register(ProjectResult)
class ProjectResultAdmin(admin.ModelAdmin):
    list_display = ("title", "project", "result_type", "display_order")
    list_filter = ("result_type",)
    search_fields = ("title", "description", "project__title")
    autocomplete_fields = ("project",)


@admin.register(ProjectLink)
class ProjectLinkAdmin(admin.ModelAdmin):
    list_display = ("label", "project", "link_type", "display_order")
    list_filter = ("link_type",)
    search_fields = ("label", "url", "project__title")
    autocomplete_fields = ("project",)

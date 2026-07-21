from django.db import migrations
from django.db.models import Q
from django.utils import timezone


REQUIRED_UNIT_MODELS = (
    ("core", "SiteSettings"),
    ("core", "HeroBanner"),
    ("core", "InstitutionalSection"),
    ("core", "SocialLink"),
    ("axes", "ResearchAxis"),
    ("portfolio", "Project"),
    ("scientific", "ScientificOutput"),
    ("news", "Post"),
    ("learning", "Course"),
    ("transparency", "TransparencyDocument"),
    ("metrics", "ImpactMetric"),
)

PUBLICATION_MODELS = (
    ("portfolio", "Project", "editorial_status"),
    ("research", "ResearchProject", "editorial_status"),
    ("research", "AcademicWork", "editorial_status"),
    ("learning", "Course", "editorial_status"),
    ("news", "Post", "status"),
    ("scientific", "ScientificOutput", "status"),
    ("transparency", "TransparencyDocument", "status"),
)


def _ids(queryset):
    return list(queryset.order_by("pk").values_list("pk", flat=True))


def preflight_and_cut(apps, schema_editor):
    database = schema_editor.connection.alias
    errors = []

    for app_label, model_name in REQUIRED_UNIT_MODELS:
        model = apps.get_model(app_label, model_name)
        missing = _ids(model.objects.using(database).filter(unit_id__isnull=True))
        if missing:
            errors.append(f"{app_label}.{model_name} sem unit: {missing}")

    for app_label, model_name, status_field in PUBLICATION_MODELS:
        model = apps.get_model(app_label, model_name)
        mismatch = model.objects.using(database).filter(
            Q(**{status_field: "published", "is_published": False})
            | (Q(is_published=True) & ~Q(**{status_field: "published"}))
        )
        mismatch_ids = _ids(mismatch)
        if mismatch_ids:
            errors.append(f"{app_label}.{model_name} com publicação contraditória: {mismatch_ids}")

    Person = apps.get_model("people", "Person")
    role_mismatch_ids = []
    for person in Person.objects.using(database).select_related("role"):
        if person.role_id and not person.institution_memberships.filter(role=person.role.name).exists():
            role_mismatch_ids.append(person.pk)
    if role_mismatch_ids:
        errors.append(f"people.Person sem membership equivalente ao role legado: {role_mismatch_ids}")

    ScientificOutput = apps.get_model("scientific", "ScientificOutput")
    external_author_ids = [
        output.pk
        for output in ScientificOutput.objects.using(database).only("pk", "authors")
        if output.authors.strip()
    ]
    if external_author_ids:
        errors.append(f"scientific.ScientificOutput com authors textual: {external_author_ids}")

    Project = apps.get_model("portfolio", "Project")
    ResearchProject = apps.get_model("research", "ResearchProject")
    legacy_projects = Project.objects.using(database).filter(
        category__slug__in=("pesquisa", "producao-cientifica")
    ).select_related("category")
    missing_destinations = []
    for project in legacy_projects:
        destination_model = ResearchProject if project.category.slug == "pesquisa" else ScientificOutput
        if not destination_model.objects.using(database).filter(legacy_portfolio_project_id=project.pk).exists():
            missing_destinations.append(project.pk)
    if missing_destinations:
        errors.append(f"portfolio.Project legado sem destino convertido: {missing_destinations}")

    if errors:
        raise RuntimeError("Corte legado bloqueado:\n- " + "\n- ".join(errors))

    ResearchProjectMember = apps.get_model("research", "ResearchProjectMember")
    ResearchProjectMember.objects.using(database).filter(
        is_coordinator=True,
    ).exclude(role="coordinator").update(role="coordinator")

    for project in legacy_projects:
        if project.category.slug == "pesquisa":
            destination = ResearchProject.objects.using(database).get(
                legacy_portfolio_project_id=project.pk
            )
            status_field = "editorial_status"
        else:
            destination = ScientificOutput.objects.using(database).get(
                legacy_portfolio_project_id=project.pk
            )
            status_field = "status"

        destination_status = project.editorial_status
        destination_is_published = destination_status == "published"
        setattr(destination, status_field, destination_status)
        destination.is_published = destination_is_published
        if destination_is_published:
            destination.published_at = project.published_at or timezone.now()
        destination.save(
            update_fields=(status_field, "is_published", "published_at")
            if destination_is_published
            else (status_field, "is_published")
        )

        project.editorial_status = "archived"
        project.is_published = False
        project.category_id = None
        project.save(update_fields=("editorial_status", "is_published", "category"))

    ProjectCategory = apps.get_model("portfolio", "ProjectCategory")
    ProjectCategory.objects.using(database).filter(
        slug__in=("pesquisa", "producao-cientifica")
    ).delete()
    ScientificOutput.objects.using(database).filter(
        output_type__in=("project", "scientific_production")
    ).update(output_type="other")

    ImpactMetric = apps.get_model("metrics", "ImpactMetric")
    ImpactMetric.objects.using(database).filter(key="eventos").delete()


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0002_add_institutional_admin_scope"),
        ("axes", "0002_researchaxis_unit"),
        ("core", "0002_herobanner_unit_institutionalsection_unit_and_more"),
        ("learning", "0003_course_unit_event_unit_learningtrack_unit"),
        ("metrics", "0002_impactmetric_unit"),
        ("news", "0002_post_unit"),
        ("people", "0001_initial"),
        ("portfolio", "0002_project_unit"),
        ("research", "0002_convert_legacy_portfolio_categories"),
        ("scientific", "0003_scientificoutput_academic_work_and_more"),
        ("transparency", "0002_transparencydocument_unit"),
    ]

    operations = [
        migrations.RunPython(preflight_and_cut, migrations.RunPython.noop),
    ]

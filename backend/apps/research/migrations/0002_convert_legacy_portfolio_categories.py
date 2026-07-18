from django.db import migrations


RESEARCH_CATEGORY = "pesquisa"
SCIENTIFIC_CATEGORY = "producao-cientifica"


def convert_legacy_projects(apps, schema_editor):
    database = schema_editor.connection.alias
    Project = apps.get_model("portfolio", "Project")
    ResearchProject = apps.get_model("research", "ResearchProject")
    ResearchProjectMember = apps.get_model("research", "ResearchProjectMember")
    ScientificOutput = apps.get_model("scientific", "ScientificOutput")

    legacy_projects = Project.objects.using(database).filter(
        category__slug__in=(RESEARCH_CATEGORY, SCIENTIFIC_CATEGORY),
    )
    missing_unit_ids = list(legacy_projects.filter(unit_id__isnull=True).values_list("id", flat=True))
    if missing_unit_ids:
        ids = ", ".join(str(project_id) for project_id in missing_unit_ids)
        raise RuntimeError(f"Projetos legados sem unidade não podem ser convertidos. IDs: {ids}")

    research_sources = legacy_projects.filter(category__slug=RESEARCH_CATEGORY)
    scientific_sources = legacy_projects.filter(category__slug=SCIENTIFIC_CATEGORY)
    research_conflicts = list(
        research_sources.filter(
            slug__in=ResearchProject.objects.using(database).values_list("slug", flat=True),
        ).values_list("id", flat=True)
    )
    scientific_conflicts = list(
        scientific_sources.filter(
            slug__in=ScientificOutput.objects.using(database).values_list("slug", flat=True),
        ).values_list("id", flat=True)
    )
    if research_conflicts or scientific_conflicts:
        conflicts = []
        if research_conflicts:
            conflicts.append(f"pesquisas IDs: {', '.join(map(str, research_conflicts))}")
        if scientific_conflicts:
            conflicts.append(f"produções IDs: {', '.join(map(str, scientific_conflicts))}")
        raise RuntimeError(f"Slugs de destino já existem para {'; '.join(conflicts)}")

    status_map = {
        "planejado": "planned",
        "em-andamento": "in_progress",
        "concluido": "completed",
        "suspenso": "suspended",
        "suspensa": "suspended",
        "cancelado": "canceled",
        "cancelada": "canceled",
    }
    for project in legacy_projects.select_related("category", "status"):
        if project.category.slug == RESEARCH_CATEGORY:
            research_project = ResearchProject.objects.using(database).create(
                unit_id=project.unit_id,
                legacy_portfolio_project_id=project.pk,
                axis_id=project.axis_id,
                title=project.title,
                slug=project.slug,
                summary=project.summary,
                project_status=status_map.get(getattr(project.status, "slug", ""), "planned"),
                editorial_status="draft",
                is_published=False,
                is_featured=False,
                display_order=project.display_order,
            )
            for member in project.team_members.all():
                ResearchProjectMember.objects.using(database).create(
                    research_project_id=research_project.id,
                    person_id=member.person_id,
                    role="coordinator" if member.is_lead else "collaborator",
                    is_coordinator=member.is_lead,
                    display_order=member.display_order,
                )
        else:
            ScientificOutput.objects.using(database).create(
                unit_id=project.unit_id,
                legacy_portfolio_project_id=project.pk,
                axis_id=project.axis_id,
                title=project.title,
                slug=project.slug,
                output_type="scientific_production",
                abstract=project.summary,
                status="draft",
                is_published=False,
                is_featured=False,
                display_order=project.display_order,
            )


def remove_converted_projects(apps, schema_editor):
    database = schema_editor.connection.alias
    ResearchProject = apps.get_model("research", "ResearchProject")
    ScientificOutput = apps.get_model("scientific", "ScientificOutput")

    ResearchProject.objects.using(database).filter(
        legacy_portfolio_project_id__isnull=False,
    ).delete()
    ScientificOutput.objects.using(database).filter(
        legacy_portfolio_project_id__isnull=False,
    ).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("portfolio", "0002_project_unit"),
        ("research", "0001_initial"),
        ("scientific", "0003_scientificoutput_academic_work_and_more"),
    ]

    operations = [
        migrations.RunPython(convert_legacy_projects, remove_converted_projects),
    ]

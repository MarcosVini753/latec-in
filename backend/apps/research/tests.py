from datetime import date
from importlib import import_module
from types import SimpleNamespace

from django.apps import apps
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError, connection, transaction
from django.db.models.deletion import ProtectedError
from django.test import RequestFactory, TestCase
from django.test.utils import CaptureQueriesContext

from apps.axes.models import ResearchAxis
from apps.accounts.models import Profile
from apps.common.models import EditorialStatus
from apps.institutional.models import InstitutionMembership, InstitutionalUnit
from apps.people.models import Person, Role
from apps.portfolio.models import Project, ProjectCategory, ProjectStatus, ProjectTeamMember
from apps.research.models import AcademicWork, AcademicWorkContributor, ResearchProject, ResearchProjectMember
from apps.research.admin import (
    AcademicWorkAdmin,
    AcademicWorkContributorAdmin,
    ResearchProjectAdmin,
    ResearchProjectMemberAdmin,
)
from apps.scientific.admin import ScientificAuthorshipAdmin, ScientificOutputAdmin
from apps.scientific.models import ScientificAuthorship, ScientificOutput


class ResearchDomainTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.labtec = InstitutionalUnit.objects.create(
            name="Laboratório LABTEC.IN",
            acronym="LABTEC.IN",
            slug="labtec-in-test",
            unit_type=InstitutionalUnit.UnitType.LABORATORY,
        )
        cls.latec = InstitutionalUnit.objects.create(
            name="Liga LATEC",
            acronym="LATEC",
            slug="latec-test",
            unit_type=InstitutionalUnit.UnitType.ACADEMIC_LEAGUE,
            parent=cls.labtec,
        )
        cls.axis = ResearchAxis.objects.create(
            unit=cls.latec,
            number=99,
            title="Eixo de testes",
            slug="eixo-de-testes",
        )
        cls.public_role = Role.objects.create(name="Pesquisador de testes", slug="pesquisador-de-testes")
        cls.person = Person.objects.create(
            full_name="Ana Pesquisadora",
            slug="ana-pesquisadora",
            role=cls.public_role,
        )
        cls.research_project = ResearchProject.objects.create(
            unit=cls.labtec,
            axis=cls.axis,
            title="Pesquisa publicada",
            slug="pesquisa-publicada",
            summary="Bioativos amazônicos.",
            start_date=date(2026, 2, 1),
            project_status=ResearchProject.ProjectStatus.IN_PROGRESS,
            editorial_status=EditorialStatus.PUBLISHED,
            is_published=True,
            is_featured=True,
        )
        ResearchProjectMember.objects.create(
            research_project=cls.research_project,
            person=cls.person,
            role=ResearchProjectMember.Role.COORDINATOR,
            is_coordinator=True,
            display_order=1,
        )
        cls.academic_work = AcademicWork.objects.create(
            unit=cls.labtec,
            research_project=cls.research_project,
            title="TCC publicado",
            slug="tcc-publicado",
            work_type=AcademicWork.WorkType.TCC,
            course="Biotecnologia",
            institution="UFAC",
            year=2026,
            abstract="Trabalho sobre bioativos.",
            editorial_status=EditorialStatus.PUBLISHED,
            is_published=True,
            is_featured=True,
        )
        AcademicWorkContributor.objects.create(
            academic_work=cls.academic_work,
            person=cls.person,
            role=AcademicWorkContributor.Role.AUTHOR,
            display_order=1,
        )
        cls.scientific_output = ScientificOutput.objects.create(
            unit=cls.labtec,
            axis=cls.axis,
            research_project=cls.research_project,
            academic_work=cls.academic_work,
            title="Artigo publicado",
            slug="artigo-publicado",
            output_type=ScientificOutput.OutputType.ARTICLE,
            authors="Autora Externa",
            publication_date=date(2026, 3, 1),
            status=EditorialStatus.PUBLISHED,
            is_published=True,
            is_featured=True,
        )
        ScientificAuthorship.objects.create(
            scientific_output=cls.scientific_output,
            person=cls.person,
            author_order=1,
            author_role="Autora principal",
        )
        ResearchProject.objects.create(
            unit=cls.latec,
            title="Pesquisa em rascunho",
            slug="pesquisa-em-rascunho",
            editorial_status=EditorialStatus.DRAFT,
            is_published=False,
        )
        AcademicWork.objects.create(
            unit=cls.latec,
            title="Trabalho em rascunho",
            slug="trabalho-em-rascunho",
            work_type=AcademicWork.WorkType.OTHER,
            editorial_status=EditorialStatus.DRAFT,
            is_published=False,
        )

    def test_research_date_range_has_friendly_and_database_validation(self):
        invalid_project = ResearchProject(
            unit=self.labtec,
            title="Datas inválidas",
            slug="datas-invalidas",
            start_date=date(2026, 2, 2),
            end_date=date(2026, 2, 1),
        )
        with self.assertRaisesMessage(ValidationError, "A data final deve ser igual ou posterior"):
            invalid_project.full_clean()

        with self.assertRaises(IntegrityError), transaction.atomic():
            ResearchProject.objects.create(
                unit=self.labtec,
                title="Constraint de datas",
                slug="constraint-de-datas",
                start_date=date(2026, 2, 2),
                end_date=date(2026, 2, 1),
            )

    def test_research_relations_enforce_uniqueness_and_protect_unit(self):
        with self.assertRaises(IntegrityError), transaction.atomic():
            ResearchProjectMember.objects.create(
                research_project=self.research_project,
                person=self.person,
                role=ResearchProjectMember.Role.RESEARCHER,
            )
        with self.assertRaises(IntegrityError), transaction.atomic():
            AcademicWorkContributor.objects.create(
                academic_work=self.academic_work,
                person=self.person,
                role=AcademicWorkContributor.Role.AUTHOR,
            )
        with self.assertRaises(IntegrityError), transaction.atomic():
            ScientificAuthorship.objects.create(
                scientific_output=self.scientific_output,
                person=self.person,
                author_order=2,
            )
        with self.assertRaises(ProtectedError):
            self.labtec.delete()

    def test_research_project_endpoint_filters_and_hides_drafts(self):
        response = self.client.get(
            "/api/v1/research-projects/",
            {
                "unit": self.labtec.slug,
                "axis": self.axis.slug,
                "project_status": ResearchProject.ProjectStatus.IN_PROGRESS,
                "year": 2026,
                "featured": "true",
                "search": "Bioativos",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual([item["slug"] for item in response.json()["results"]], [self.research_project.slug])
        item = response.json()["results"][0]
        self.assertEqual(set(item["unit"]), {"name", "acronym", "slug", "unit_type"})
        self.assertEqual(item["axis"]["slug"], self.axis.slug)
        self.assertEqual(item["team_members"][0]["person"]["slug"], self.person.slug)
        self.assertEqual(self.client.get("/api/v1/research-projects/pesquisa-em-rascunho/").status_code, 404)

    def test_featured_false_filters_and_invalid_public_filters_return_400(self):
        non_featured = ResearchProject.objects.create(
            unit=self.labtec,
            title="Pesquisa sem destaque",
            slug="pesquisa-sem-destaque",
            editorial_status=EditorialStatus.PUBLISHED,
            is_published=True,
            is_featured=False,
        )

        response = self.client.get("/api/v1/research-projects/", {"featured": "false"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual([item["slug"] for item in response.json()["results"]], [non_featured.slug])
        self.assertEqual(
            self.client.get("/api/v1/research-projects/", {"featured": "talvez"}).status_code,
            400,
        )
        for endpoint in ("research-projects", "academic-works", "scientific-outputs"):
            with self.subTest(endpoint=endpoint):
                self.assertEqual(self.client.get(f"/api/v1/{endpoint}/", {"year": "abc"}).status_code, 400)

    def test_academic_work_endpoint_filters_and_returns_nested_summaries(self):
        response = self.client.get(
            "/api/v1/academic-works/",
            {
                "unit": self.labtec.slug,
                "work_type": AcademicWork.WorkType.TCC,
                "year": 2026,
                "featured": "1",
                "search": "bioativos",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual([item["slug"] for item in response.json()["results"]], [self.academic_work.slug])
        item = response.json()["results"][0]
        self.assertEqual(item["research_project"]["slug"], self.research_project.slug)
        self.assertEqual(item["contributors"][0]["person"]["slug"], self.person.slug)
        self.assertEqual(self.client.get("/api/v1/academic-works/trabalho-em-rascunho/").status_code, 404)

    def test_scientific_output_keeps_external_authors_and_structured_authorship(self):
        response = self.client.get(f"/api/v1/scientific-outputs/{self.scientific_output.slug}/")

        self.assertEqual(response.status_code, 200)
        item = response.json()
        self.assertEqual(item["authors"], "Autora Externa")
        self.assertEqual(item["authorships"][0]["person"]["slug"], self.person.slug)
        self.assertEqual(item["research_project"]["slug"], self.research_project.slug)
        self.assertEqual(item["academic_work"]["slug"], self.academic_work.slug)

    def test_nested_endpoints_do_not_add_queries_per_item(self):
        initial_counts = {}
        for endpoint in ("research-projects", "academic-works", "scientific-outputs"):
            with CaptureQueriesContext(connection) as queries:
                self.client.get(f"/api/v1/{endpoint}/")
            initial_counts[endpoint] = len(queries)

        second_person = Person.objects.create(full_name="Bia Pesquisadora", slug="bia-pesquisadora")
        second_research = ResearchProject.objects.create(
            unit=self.labtec,
            axis=self.axis,
            title="Segunda pesquisa",
            slug="segunda-pesquisa",
            editorial_status=EditorialStatus.PUBLISHED,
            is_published=True,
        )
        ResearchProjectMember.objects.create(
            research_project=second_research,
            person=second_person,
            display_order=1,
        )
        second_work = AcademicWork.objects.create(
            unit=self.labtec,
            research_project=second_research,
            title="Segundo trabalho",
            slug="segundo-trabalho",
            work_type=AcademicWork.WorkType.OTHER,
            editorial_status=EditorialStatus.PUBLISHED,
            is_published=True,
        )
        AcademicWorkContributor.objects.create(
            academic_work=second_work,
            person=second_person,
            role=AcademicWorkContributor.Role.AUTHOR,
        )
        second_output = ScientificOutput.objects.create(
            unit=self.labtec,
            research_project=second_research,
            academic_work=second_work,
            title="Segundo artigo",
            slug="segundo-artigo",
            output_type=ScientificOutput.OutputType.ARTICLE,
            status=EditorialStatus.PUBLISHED,
            is_published=True,
        )
        ScientificAuthorship.objects.create(
            scientific_output=second_output,
            person=second_person,
            author_order=1,
        )

        for endpoint, initial_count in initial_counts.items():
            with self.subTest(endpoint=endpoint), CaptureQueriesContext(connection) as queries:
                self.client.get(f"/api/v1/{endpoint}/")
            self.assertEqual(len(queries), initial_count)

    def test_openapi_documents_new_public_filters(self):
        schema = self.client.get("/api/schema/").content.decode()

        self.assertIn("/api/v1/research-projects/", schema)
        self.assertIn("/api/v1/academic-works/", schema)
        self.assertIn("project_status", schema)
        self.assertIn("work_type", schema)


class LegacyCategoryConversionTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.unit = InstitutionalUnit.objects.create(
            name="Unidade de migração",
            acronym="MIG",
            slug="unidade-de-migracao",
            unit_type=InstitutionalUnit.UnitType.RESEARCH_GROUP,
        )
        cls.person = Person.objects.create(full_name="Pessoa da migração", slug="pessoa-da-migracao")
        cls.status = ProjectStatus.objects.create(name="Em andamento da migração", slug="em-andamento")
        cls.research_category = ProjectCategory.objects.create(name="Pesquisa da migração", slug="pesquisa")
        cls.scientific_category = ProjectCategory.objects.create(
            name="Produção científica da migração",
            slug="producao-cientifica",
        )

    def setUp(self):
        self.migration = import_module("apps.research.migrations.0002_convert_legacy_portfolio_categories")
        self.schema_editor = SimpleNamespace(connection=connection)

    def test_conversion_is_reversible_and_preserves_legacy_sources(self):
        research_source = Project.objects.create(
            unit=self.unit,
            title="Pesquisa legada",
            slug="pesquisa-legada",
            category=self.research_category,
            status=self.status,
            summary="Resumo preservado.",
            editorial_status=EditorialStatus.PUBLISHED,
            is_published=True,
        )
        ProjectTeamMember.objects.create(
            project=research_source,
            person=self.person,
            is_lead=True,
            display_order=1,
        )
        scientific_source = Project.objects.create(
            unit=self.unit,
            title="Produção legada",
            slug="producao-legada",
            category=self.scientific_category,
            summary="Resumo científico.",
            editorial_status=EditorialStatus.PUBLISHED,
            is_published=True,
        )
        unrelated_research = ResearchProject.objects.create(
            unit=self.unit,
            title="Pesquisa nativa",
            slug="pesquisa-nativa",
        )

        self.migration.convert_legacy_projects(apps, self.schema_editor)

        converted_research = ResearchProject.objects.get(slug=research_source.slug)
        self.assertEqual(converted_research.legacy_portfolio_project_id, research_source.pk)
        self.assertEqual(converted_research.project_status, ResearchProject.ProjectStatus.IN_PROGRESS)
        self.assertEqual(converted_research.summary, research_source.summary)
        self.assertEqual(converted_research.editorial_status, EditorialStatus.DRAFT)
        self.assertFalse(converted_research.is_published)
        member = converted_research.team_members.get()
        self.assertEqual(member.role, ResearchProjectMember.Role.COORDINATOR)
        self.assertTrue(member.is_coordinator)
        converted_output = ScientificOutput.objects.get(slug=scientific_source.slug)
        self.assertEqual(converted_output.legacy_portfolio_project_id, scientific_source.pk)
        self.assertEqual(converted_output.output_type, ScientificOutput.OutputType.SCIENTIFIC_PRODUCTION)
        self.assertEqual(converted_output.status, EditorialStatus.DRAFT)
        self.assertFalse(converted_output.is_published)
        self.assertEqual(Project.objects.filter(pk__in=(research_source.pk, scientific_source.pk)).count(), 2)

        converted_research.slug = "pesquisa-derivada-renomeada"
        converted_research.save(update_fields=("slug",))
        native_research = ResearchProject.objects.create(
            unit=self.unit,
            title="Pesquisa nativa no slug antigo",
            slug=research_source.slug,
        )
        converted_output.slug = "producao-derivada-renomeada"
        converted_output.save(update_fields=("slug",))
        native_output = ScientificOutput.objects.create(
            unit=self.unit,
            title="Produção nativa no slug antigo",
            slug=scientific_source.slug,
            output_type=ScientificOutput.OutputType.ARTICLE,
        )

        self.migration.remove_converted_projects(apps, self.schema_editor)

        self.assertFalse(ResearchProject.objects.filter(pk=converted_research.pk).exists())
        self.assertFalse(ScientificOutput.objects.filter(pk=converted_output.pk).exists())
        self.assertTrue(ResearchProject.objects.filter(pk=native_research.pk).exists())
        self.assertTrue(ScientificOutput.objects.filter(pk=native_output.pk).exists())
        self.assertTrue(ResearchProject.objects.filter(pk=unrelated_research.pk).exists())
        self.assertEqual(Project.objects.filter(pk__in=(research_source.pk, scientific_source.pk)).count(), 2)

    def test_conversion_preserves_compatible_suspended_and_canceled_statuses(self):
        suspended = ProjectStatus.objects.create(name="Suspensa", slug="suspensa")
        canceled = ProjectStatus.objects.create(name="Cancelado", slug="cancelado")
        Project.objects.create(
            unit=self.unit,
            title="Pesquisa suspensa",
            slug="pesquisa-suspensa",
            category=self.research_category,
            status=suspended,
        )
        Project.objects.create(
            unit=self.unit,
            title="Pesquisa cancelada",
            slug="pesquisa-cancelada",
            category=self.research_category,
            status=canceled,
        )

        self.migration.convert_legacy_projects(apps, self.schema_editor)

        self.assertEqual(
            ResearchProject.objects.get(slug="pesquisa-suspensa").project_status,
            ResearchProject.ProjectStatus.SUSPENDED,
        )
        self.assertEqual(
            ResearchProject.objects.get(slug="pesquisa-cancelada").project_status,
            ResearchProject.ProjectStatus.CANCELED,
        )

    def test_conversion_preflight_reports_projects_without_unit(self):
        project = Project.objects.create(
            title="Pesquisa sem unidade",
            slug="pesquisa-sem-unidade-na-migracao",
            category=self.research_category,
        )

        with self.assertRaisesMessage(RuntimeError, f"IDs: {project.id}"):
            self.migration.convert_legacy_projects(apps, self.schema_editor)

    def test_conversion_preflight_reports_slug_collisions_without_writing(self):
        source = Project.objects.create(
            unit=self.unit,
            title="Pesquisa com colisão",
            slug="pesquisa-com-colisao",
            category=self.research_category,
        )
        ResearchProject.objects.create(
            unit=self.unit,
            title="Pesquisa já existente",
            slug=source.slug,
        )

        with self.assertRaisesMessage(RuntimeError, f"pesquisas IDs: {source.id}"):
            self.migration.convert_legacy_projects(apps, self.schema_editor)

        self.assertEqual(ResearchProject.objects.filter(slug=source.slug).count(), 1)


class ResearchAdminScopeTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.labtec = InstitutionalUnit.objects.create(
            name="LABTEC.IN",
            acronym="LABTEC.IN",
            slug="labtec-in",
            unit_type=InstitutionalUnit.UnitType.LABORATORY,
        )
        cls.latec = InstitutionalUnit.objects.create(
            name="LATEC",
            acronym="LATEC",
            slug="latec",
            unit_type=InstitutionalUnit.UnitType.ACADEMIC_LEAGUE,
            parent=cls.labtec,
        )
        cls.axis = ResearchAxis.objects.create(
            unit=cls.latec,
            number=201,
            title="Eixo permitido no Admin",
            slug="eixo-permitido-admin",
        )
        cls.other_axis = ResearchAxis.objects.create(
            unit=cls.latec,
            number=202,
            title="Outro eixo no Admin",
            slug="outro-eixo-admin",
        )
        cls.person = Person.objects.create(full_name="Pessoa do Admin", slug="pessoa-do-admin")
        cls.mentor_person = Person.objects.create(full_name="Mentora do Admin", slug="mentora-do-admin")
        InstitutionMembership.objects.create(person=cls.person, unit=cls.latec, role="Pesquisador")
        InstitutionMembership.objects.create(person=cls.mentor_person, unit=cls.latec, role="Mentor")
        cls.axis.mentorships.create(person=cls.mentor_person)

        cls.editor_user = get_user_model().objects.create_user("research_editor", is_staff=True)
        cls.editor_profile = Profile.objects.create(user=cls.editor_user, role=Profile.AdminRole.EDITOR)
        cls.editor_profile.authorized_units.add(cls.latec)
        cls.mentor_user = get_user_model().objects.create_user("research_mentor", is_staff=True)
        Profile.objects.create(
            user=cls.mentor_user,
            person=cls.mentor_person,
            role=Profile.AdminRole.MENTOR,
            primary_unit=cls.latec,
        )

    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.post("/admin/")
        self.request.user = self.editor_user

    def test_scoped_editor_can_create_research_graph_as_draft(self):
        project_admin = ResearchProjectAdmin(ResearchProject, admin.site)
        member_admin = ResearchProjectMemberAdmin(ResearchProjectMember, admin.site)
        work_admin = AcademicWorkAdmin(AcademicWork, admin.site)
        contributor_admin = AcademicWorkContributorAdmin(AcademicWorkContributor, admin.site)
        output_admin = ScientificOutputAdmin(ScientificOutput, admin.site)
        authorship_admin = ScientificAuthorshipAdmin(ScientificAuthorship, admin.site)

        project = ResearchProject(
            unit=self.latec,
            axis=self.axis,
            title="Pesquisa criada no Admin",
            slug="pesquisa-criada-no-admin",
        )
        project_admin.save_model(self.request, project, form=None, change=False)
        member = ResearchProjectMember(
            research_project=project,
            person=self.person,
            role=ResearchProjectMember.Role.RESEARCHER,
        )
        member_admin.save_model(self.request, member, form=None, change=False)
        work = AcademicWork(
            unit=self.latec,
            research_project=project,
            title="Trabalho criado no Admin",
            slug="trabalho-criado-no-admin",
            work_type=AcademicWork.WorkType.TCC,
        )
        work_admin.save_model(self.request, work, form=None, change=False)
        contributor = AcademicWorkContributor(
            academic_work=work,
            person=self.person,
            role=AcademicWorkContributor.Role.AUTHOR,
        )
        contributor_admin.save_model(self.request, contributor, form=None, change=False)
        output = ScientificOutput(
            unit=self.latec,
            axis=self.axis,
            research_project=project,
            academic_work=work,
            title="Produção criada no Admin",
            slug="producao-criada-no-admin",
            output_type=ScientificOutput.OutputType.ARTICLE,
        )
        output_admin.save_model(self.request, output, form=None, change=False)
        authorship = ScientificAuthorship(
            scientific_output=output,
            person=self.person,
            author_order=1,
        )
        authorship_admin.save_model(self.request, authorship, form=None, change=False)

        self.assertEqual(project.editorial_status, EditorialStatus.DRAFT)
        self.assertFalse(project.is_published)
        self.assertTrue(project_admin.get_queryset(self.request).filter(pk=project.pk).exists())
        self.assertTrue(work_admin.get_queryset(self.request).filter(pk=work.pk).exists())
        self.assertTrue(output_admin.get_queryset(self.request).filter(pk=output.pk).exists())
        self.assertTrue(authorship_admin.get_queryset(self.request).filter(pk=authorship.pk).exists())

    def test_mentor_querysets_and_related_choices_are_limited_to_own_axis(self):
        own_project = ResearchProject.objects.create(
            unit=self.latec,
            axis=self.axis,
            title="Pesquisa do eixo mentorado",
            slug="pesquisa-eixo-mentorado",
        )
        ResearchProject.objects.create(
            unit=self.latec,
            axis=self.other_axis,
            title="Pesquisa de outro eixo",
            slug="pesquisa-outro-eixo",
        )
        request = self.factory.get("/admin/")
        request.user = self.mentor_user
        project_admin = ResearchProjectAdmin(ResearchProject, admin.site)
        output_admin = ScientificOutputAdmin(ScientificOutput, admin.site)

        self.assertEqual(
            set(project_admin.get_queryset(request).values_list("slug", flat=True)),
            {own_project.slug},
        )
        research_project_field = ScientificOutput._meta.get_field("research_project")
        choices = output_admin.formfield_for_foreignkey(research_project_field, request).queryset
        self.assertEqual(set(choices.values_list("slug", flat=True)), {own_project.slug})

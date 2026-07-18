import shutil
import tempfile

from django.core.management import call_command
from django.db.models import Count
from django.test import TestCase, override_settings
from django.utils.text import slugify

from apps.axes.models import AxisMentorship, ResearchAxis
from apps.common.models import EditorialStatus
from apps.core.models import HeroBanner, InstitutionalSection, SiteSettings, SocialLink
from apps.institutional.models import InstitutionMembership, InstitutionalUnit
from apps.learning.models import Course, CourseMaterial, LearningTrack
from apps.metrics.models import ImpactMetric
from apps.news.models import Post
from apps.partnerships.models import ContactMessage, Partner
from apps.people.models import Person, Role
from apps.portfolio.models import Project, ProjectCategory, ProjectResult, ProjectStatus, ProjectTeamMember
from apps.research.models import ResearchProject, ResearchProjectMember
from apps.scientific.models import ScientificOutput


TEST_MEDIA_ROOT = tempfile.mkdtemp(prefix="latec-test-media-")


@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class CmsApiTests(TestCase):
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEST_MEDIA_ROOT, ignore_errors=True)

    @classmethod
    def setUpTestData(cls):
        call_command("seed_initial_data", verbosity=0)

    def test_seed_initial_data_is_idempotent(self):
        expected_counts = {
            InstitutionalUnit: 2,
            InstitutionMembership: 43,
            Role: 7,
            Person: 33,
            ResearchAxis: 7,
            AxisMentorship: 9,
            Project: 2,
            ProjectResult: 3,
            ProjectTeamMember: 5,
            ResearchProject: 1,
            ResearchProjectMember: 2,
            Post: 2,
            Course: 2,
            CourseMaterial: 1,
            ImpactMetric: 7,
            SiteSettings: 1,
            HeroBanner: 1,
            InstitutionalSection: 3,
        }

        call_command("seed_initial_data", verbosity=0)

        for model, expected_count in expected_counts.items():
            with self.subTest(model=model.__name__):
                self.assertEqual(model.objects.count(), expected_count)

        duplicate_memberships = (
            InstitutionMembership.objects.values("person", "unit", "role")
            .annotate(total=Count("id"))
            .filter(total__gt=1)
        )
        self.assertFalse(duplicate_memberships.exists())

    def test_seed_creates_institutional_hierarchy_and_assigns_core_content(self):
        labtec = InstitutionalUnit.objects.get(slug="labtec-in")
        latec = InstitutionalUnit.objects.get(slug="latec")

        self.assertEqual(labtec.unit_type, InstitutionalUnit.UnitType.LABORATORY)
        self.assertIsNone(labtec.parent)
        self.assertEqual(latec.unit_type, InstitutionalUnit.UnitType.ACADEMIC_LEAGUE)
        self.assertEqual(latec.parent, labtec)

        settings = SiteSettings.objects.get()
        self.assertEqual(settings.site_name, "LABTEC.IN")
        self.assertEqual(settings.unit, labtec)
        self.assertFalse(HeroBanner.objects.exclude(unit=labtec).exists())
        self.assertFalse(InstitutionalSection.objects.exclude(unit=labtec).exists())

    def test_seed_assigns_content_and_basic_memberships_to_units(self):
        labtec = InstitutionalUnit.objects.get(slug="labtec-in")
        latec = InstitutionalUnit.objects.get(slug="latec")

        self.assertEqual(ResearchAxis.objects.filter(unit=latec).count(), 7)
        self.assertFalse(Post.objects.exclude(unit=latec).exists())
        self.assertFalse(Course.objects.exclude(unit=latec).exists())
        self.assertFalse(Project.objects.exclude(unit=latec).exists())
        self.assertFalse(ResearchProject.objects.exclude(unit=latec).exists())
        self.assertFalse(LearningTrack.objects.exclude(unit=labtec).exists())
        self.assertFalse(ImpactMetric.objects.exclude(unit=labtec).exists())

        self.assertEqual(
            InstitutionMembership.objects.filter(unit=latec, person__role__slug="ligante").count(),
            22,
        )
        self.assertEqual(
            InstitutionMembership.objects.filter(
                unit=labtec,
                person__role__slug__in=("professor", "pesquisador", "estagiario"),
            ).count(),
            10,
        )
        coordinator = Person.objects.get(slug=slugify("Marta Adelino"))
        self.assertEqual(
            set(coordinator.institution_memberships.values_list("unit__slug", "role")),
            {
                ("labtec-in", "Coordenadora"),
                ("latec", "Coordenadora"),
                ("latec", "Mentor"),
            },
        )
        self.assertEqual(
            InstitutionMembership.objects.filter(unit=latec, role="Mentor").count(),
            9,
        )

    def test_seed_preserves_manual_project_unit_classification(self):
        project = Project.objects.order_by("pk").first()
        labtec = InstitutionalUnit.objects.get(slug="labtec-in")
        project.unit = labtec
        project.save(update_fields=["unit"])

        call_command("seed_initial_data", verbosity=0)

        project.refresh_from_db()
        self.assertEqual(project.unit, labtec)

    def test_seed_keeps_research_draft_state_and_out_of_legacy_portfolio(self):
        research = ResearchProject.objects.get(slug="pesquisa-de-bioativos-da-amazonia")
        research.editorial_status = EditorialStatus.ARCHIVED
        research.is_published = False
        research.save(update_fields=("editorial_status", "is_published"))

        call_command("seed_initial_data", verbosity=0)

        research.refresh_from_db()
        self.assertEqual(research.editorial_status, EditorialStatus.ARCHIVED)
        self.assertFalse(research.is_published)
        self.assertFalse(Project.objects.filter(slug=research.slug).exists())

    def test_seed_corrects_legacy_labels_without_changing_public_slugs(self):
        hero = HeroBanner.objects.get(title="Biotecnologia, biodiversidade e inovação")
        coordinator = Person.objects.get(slug=slugify("Marta Adelino"))
        professor_role = Role.objects.get(slug="professor")
        graduate_role = Role.objects.get(slug="egresso")

        self.assertTrue(hero.subtitle.startswith("Um laboratório"))
        self.assertIn("LABTEC.IN e da LATEC", coordinator.short_bio)
        self.assertIn("LABTEC.IN", professor_role.description)
        self.assertIn("LATEC", professor_role.description)
        self.assertIn("LABTEC.IN ou a LATEC", graduate_role.description)
        self.assertEqual(
            set(Post.objects.values_list("slug", flat=True)),
            {
                "coordenadora-do-latecin-e-premiada-por-inovacao-tecnologica",
                "latecin-participa-do-congresso-nacional-de-inovacao",
            },
        )
        self.assertFalse(Post.objects.filter(title__contains="LATEC.IN").exists())

    def test_seed_reuses_legacy_site_settings_without_losing_custom_data(self):
        SiteSettings.objects.all().delete()
        legacy_settings = SiteSettings.objects.create(
            site_name="LATEC.IN",
            description="Descrição institucional revisada.",
            contact_email="contato@example.com",
        )

        call_command("seed_initial_data", verbosity=0)

        settings = SiteSettings.objects.get()
        self.assertEqual(settings.pk, legacy_settings.pk)
        self.assertEqual(settings.site_name, "LABTEC.IN")
        self.assertEqual(settings.unit.slug, "labtec-in")
        self.assertEqual(settings.description, "Descrição institucional revisada.")
        self.assertEqual(settings.contact_email, "contato@example.com")

    def test_institutional_units_endpoint_only_exposes_active_public_units(self):
        private_unit = InstitutionalUnit.objects.create(
            name="Unidade privada",
            acronym="PRIVADA",
            slug="unidade-privada",
            unit_type=InstitutionalUnit.UnitType.INITIATIVE,
            is_public=False,
        )
        InstitutionalUnit.objects.create(
            name="Unidade inativa",
            acronym="INATIVA",
            slug="unidade-inativa",
            unit_type=InstitutionalUnit.UnitType.PROGRAM,
            is_active=False,
        )
        InstitutionalUnit.objects.create(
            name="Filha pública",
            acronym="FILHA",
            slug="filha-publica",
            unit_type=InstitutionalUnit.UnitType.INITIATIVE,
            parent=private_unit,
        )

        response = self.client.get("/api/v1/institutional-units/")

        self.assertEqual(response.status_code, 200)
        slugs = {item["slug"] for item in response.json()["results"]}
        self.assertEqual(slugs, {"labtec-in", "latec", "filha-publica"})
        self.assertEqual(self.client.get("/api/v1/institutional-units/unidade-privada/").status_code, 404)
        self.assertEqual(self.client.get("/api/v1/institutional-units/unidade-inativa/").status_code, 404)
        public_child = next(item for item in response.json()["results"] if item["slug"] == "filha-publica")
        self.assertIsNone(public_child["parent"])

        latec_response = self.client.get("/api/v1/institutional-units/latec/")
        self.assertEqual(latec_response.status_code, 200)
        self.assertEqual(latec_response.json()["parent"]["slug"], "labtec-in")

    def test_home_only_returns_labtec_content(self):
        labtec = InstitutionalUnit.objects.get(slug="labtec-in")
        latec = InstitutionalUnit.objects.get(slug="latec")
        SiteSettings.objects.create(unit=latec, site_name="LATEC", is_active=True)
        SiteSettings.objects.create(site_name="Sem unidade", is_active=True)
        HeroBanner.objects.create(unit=latec, title="Hero LATEC", is_published=True)
        HeroBanner.objects.create(title="Hero sem unidade", is_published=True)
        InstitutionalSection.objects.create(
            unit=latec,
            section_type=InstitutionalSection.SectionType.HISTORY,
            title="Seção LATEC",
            slug="secao-latec",
            content="Conteúdo da Liga.",
            is_published=True,
        )
        InstitutionalSection.objects.create(
            section_type=InstitutionalSection.SectionType.HISTORY,
            title="Seção sem unidade",
            slug="secao-sem-unidade",
            content="Conteúdo ainda não classificado.",
            is_published=True,
        )
        SocialLink.objects.create(unit=labtec, label="LABTEC.IN", url="https://labtec.example.com")
        SocialLink.objects.create(unit=latec, label="LATEC", url="https://latec.example.com")
        SocialLink.objects.create(label="Sem unidade", url="https://example.com")

        response = self.client.get("/api/v1/site/home/")

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["settings"]["site_name"], "LABTEC.IN")
        self.assertEqual(data["settings"]["unit"]["slug"], "labtec-in")
        for collection in ("heroes", "sections", "social_links"):
            self.assertTrue(data[collection])
            self.assertTrue(all(item["unit"]["slug"] == "labtec-in" for item in data[collection]))
        self.assertNotIn("Hero LATEC", {item["title"] for item in data["heroes"]})
        self.assertNotIn("Hero sem unidade", {item["title"] for item in data["heroes"]})
        self.assertNotIn("Seção LATEC", {item["title"] for item in data["sections"]})
        self.assertNotIn("Seção sem unidade", {item["title"] for item in data["sections"]})
        self.assertEqual([item["label"] for item in data["social_links"]], ["LABTEC.IN"])

    def test_public_endpoints_respond(self):
        urls = [
            "/api/v1/site/home/",
            "/api/v1/site/settings/",
            "/api/v1/institutional-units/",
            "/api/v1/institutional-units/labtec-in/",
            "/api/v1/people/",
            "/api/v1/axes/",
            "/api/v1/projects/",
            f"/api/v1/projects/{slugify('Fábrica de Ensino: Bootcamp de Startups')}/",
            "/api/v1/posts/",
            f"/api/v1/posts/{slugify('Coordenadora do LATEC.IN é premiada por inovação tecnológica')}/",
            "/api/v1/courses/",
            f"/api/v1/courses/{slugify('Nanotecnologias de cosméticos')}/",
            "/api/v1/transparency-documents/",
            "/api/v1/partners/",
            "/api/v1/metrics/impact/",
        ]

        for url in urls:
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 200)

    def test_public_api_hides_unpublished_items(self):
        category = ProjectCategory.objects.get(slug=slugify("Ensino"))
        status = ProjectStatus.objects.get(slug=slugify("Planejado"))
        Project.objects.create(
            title="Projeto em rascunho",
            slug="projeto-em-rascunho",
            category=category,
            status=status,
            summary="Ainda não deve aparecer publicamente.",
            editorial_status=EditorialStatus.DRAFT,
            is_published=False,
        )

        response = self.client.get("/api/v1/projects/")

        self.assertEqual(response.status_code, 200)
        titles = [item["title"] for item in response.json()["results"]]
        self.assertNotIn("Projeto em rascunho", titles)

    def test_public_filters_by_featured_year_category_and_search(self):
        response = self.client.get(
            "/api/v1/projects/",
            {"featured": "true", "year": "2025", "category": slugify("Ensino"), "search": "Bootcamp"},
        )

        self.assertEqual(response.status_code, 200)
        titles = [item["title"] for item in response.json()["results"]]
        self.assertEqual(titles, ["Fábrica de Ensino: Bootcamp de Startups"])

    def test_public_endpoints_filter_by_unit_and_keep_unassigned_content_compatible(self):
        labtec = InstitutionalUnit.objects.get(slug="labtec-in")
        latec = InstitutionalUnit.objects.get(slug="latec")
        category = ProjectCategory.objects.get(slug=slugify("Ensino"))
        project_status = ProjectStatus.objects.get(slug=slugify("Em andamento"))
        Project.objects.create(
            unit=labtec,
            title="Projeto do LABTEC.IN",
            slug="projeto-do-labtec-in",
            category=category,
            status=project_status,
            editorial_status=EditorialStatus.PUBLISHED,
            is_published=True,
        )
        unassigned_project = Project.objects.create(
            title="Projeto sem unidade",
            slug="projeto-sem-unidade",
            category=category,
            status=project_status,
            editorial_status=EditorialStatus.PUBLISHED,
            is_published=True,
        )
        Post.objects.create(
            unit=labtec,
            title="Notícia do LABTEC.IN",
            slug="noticia-do-labtec-in",
            content="Conteúdo institucional.",
            status=EditorialStatus.PUBLISHED,
            is_published=True,
        )
        Course.objects.create(
            unit=labtec,
            title="Curso do LABTEC.IN",
            slug="curso-do-labtec-in",
            editorial_status=EditorialStatus.PUBLISHED,
            is_published=True,
        )
        for unit in (labtec, latec):
            ScientificOutput.objects.create(
                unit=unit,
                title=f"Produção {unit.acronym}",
                slug=f"producao-{unit.slug}",
                output_type=ScientificOutput.OutputType.ARTICLE,
                status=EditorialStatus.PUBLISHED,
                is_published=True,
            )

        for endpoint in ("projects", "posts", "courses", "scientific-outputs"):
            for unit_slug in ("labtec-in", "latec"):
                with self.subTest(endpoint=endpoint, unit=unit_slug):
                    response = self.client.get(f"/api/v1/{endpoint}/", {"unit": unit_slug})
                    self.assertEqual(response.status_code, 200)
                    results = response.json()["results"]
                    self.assertTrue(results)
                    self.assertTrue(all(item["unit"]["slug"] == unit_slug for item in results))
                    self.assertEqual(
                        set(results[0]["unit"]),
                        {"name", "acronym", "slug", "unit_type"},
                    )

        unfiltered_response = self.client.get("/api/v1/projects/")
        unassigned_item = next(
            item for item in unfiltered_response.json()["results"] if item["slug"] == unassigned_project.slug
        )
        self.assertIsNone(unassigned_item["unit"])
        self.assertEqual(self.client.get(f"/api/v1/projects/{unassigned_project.slug}/").status_code, 200)

    def test_partner_can_belong_to_multiple_units_and_filter_by_each_one(self):
        units = list(InstitutionalUnit.objects.filter(slug__in=("labtec-in", "latec")))
        partner = Partner.objects.create(name="UFAC", slug="ufac")
        partner.units.add(*units)

        response = self.client.get(f"/api/v1/partners/{partner.slug}/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual({item["slug"] for item in response.json()["units"]}, {"labtec-in", "latec"})
        for unit in units:
            with self.subTest(unit=unit.slug):
                filtered = self.client.get("/api/v1/partners/", {"unit": unit.slug})
                self.assertEqual(filtered.status_code, 200)
                self.assertIn(partner.slug, {item["slug"] for item in filtered.json()["results"]})

    def test_contact_endpoint_only_allows_public_creation(self):
        self.assertEqual(self.client.get("/api/v1/contact/").status_code, 405)

        response = self.client.post(
            "/api/v1/contact/",
            {
                "contact_type": "partnership",
                "subject": "Parceria institucional",
                "name": "Pessoa Interessada",
                "email": "pessoa@example.com",
                "organization": "UFAC",
                "message": "Gostaria de conversar sobre uma parceria.",
            },
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(ContactMessage.objects.count(), 1)
        self.assertEqual(ContactMessage.objects.get().contact_type, ContactMessage.ContactType.PARTNERSHIP)

    def test_openapi_schema_is_available(self):
        response = self.client.get("/api/schema/")

        self.assertEqual(response.status_code, 200)
        self.assertIn("LABTEC.IN API", response.content.decode())

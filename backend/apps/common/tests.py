import shutil
import tempfile

from django.core.management import call_command
from django.test import TestCase, override_settings
from django.utils.text import slugify

from apps.axes.models import AxisMentorship, ResearchAxis
from apps.common.models import EditorialStatus
from apps.core.models import HeroBanner, InstitutionalSection, SiteSettings
from apps.institutional.models import InstitutionalUnit
from apps.learning.models import Course, CourseMaterial
from apps.metrics.models import ImpactMetric
from apps.news.models import Post
from apps.partnerships.models import ContactMessage
from apps.people.models import Person, Role
from apps.portfolio.models import Project, ProjectCategory, ProjectResult, ProjectStatus, ProjectTeamMember


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
            Role: 7,
            Person: 33,
            ResearchAxis: 7,
            AxisMentorship: 9,
            Project: 3,
            ProjectResult: 5,
            ProjectTeamMember: 7,
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

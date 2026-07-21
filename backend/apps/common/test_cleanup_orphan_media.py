import shutil
import tempfile
from io import StringIO
from pathlib import Path

from django.conf import settings
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import call_command
from django.core.management.base import CommandError
from django.db import connection
from django.db.migrations.executor import MigrationExecutor
from django.test import TestCase, TransactionTestCase, override_settings

from apps.institutional.models import InstitutionalUnit
from apps.learning.models import Course, CourseMaterial


class CleanupOrphanMediaCommandTests(TestCase):
    def setUp(self):
        self.media_root = tempfile.mkdtemp(prefix="latec-orphan-media-")
        self.settings_override = override_settings(MEDIA_ROOT=self.media_root)
        self.settings_override.enable()

        unit = InstitutionalUnit.objects.create(
            name="Unidade de teste",
            acronym="UT",
            slug="unidade-limpeza-midia",
            unit_type=InstitutionalUnit.UnitType.LABORATORY,
        )
        course = Course.objects.create(unit=unit, title="Curso", slug="curso-limpeza-midia")
        self.material = CourseMaterial.objects.create(
            course=course,
            title="Material referenciado",
            file=SimpleUploadedFile("referenciado.txt", b"conteudo"),
        )
        CourseMaterial.objects.create(
            course=course,
            title="Material ausente",
            file="learning/materials/ausente.txt",
        )
        self.referenced_path = Path(self.media_root, self.material.file.name)
        self.orphan_path = Path(self.media_root, "uploads", "orfao.txt")
        self.orphan_path.parent.mkdir(parents=True)
        self.orphan_path.write_bytes(b"orfao")

    def tearDown(self):
        self.settings_override.disable()
        shutil.rmtree(self.media_root, ignore_errors=True)

    def test_dry_run_reports_inventory_without_deleting(self):
        output = StringIO()

        call_command("cleanup_orphan_media", stdout=output)

        report = output.getvalue()
        self.assertIn("Arquivos órfãos: 1", report)
        self.assertIn("- uploads/orfao.txt", report)
        self.assertIn("Referências sem arquivo: 1", report)
        self.assertIn("- learning/materials/ausente.txt", report)
        self.assertIn("Dry-run: nenhum arquivo foi removido", report)
        self.assertTrue(self.orphan_path.exists())
        self.assertTrue(self.referenced_path.exists())

    def test_delete_removes_only_orphans(self):
        output = StringIO()

        call_command(
            "cleanup_orphan_media",
            delete=True,
            confirm_root=self.media_root,
            stdout=output,
        )

        self.assertIn("Arquivos removidos: 1", output.getvalue())
        self.assertFalse(self.orphan_path.exists())
        self.assertTrue(self.referenced_path.exists())

    def test_rejects_a_broad_media_root(self):
        with override_settings(MEDIA_ROOT=settings.BASE_DIR):
            with self.assertRaisesMessage(CommandError, "diretório dedicado"):
                call_command("cleanup_orphan_media", delete=True)

    def test_custom_media_root_requires_exact_confirmation(self):
        with self.assertRaisesMessage(CommandError, "--confirm-root"):
            call_command("cleanup_orphan_media", delete=True)

        with self.assertRaisesMessage(CommandError, "--confirm-root"):
            call_command(
                "cleanup_orphan_media",
                delete=True,
                confirm_root=str(Path(self.media_root).parent),
            )


class LegacyMediaHubCleanupMigrationTests(TransactionTestCase):
    migrate_from = [("research", "0004_alter_academicwork_options_and_more")]
    migrate_to = [("research", "0005_drop_legacy_mediahub_table")]

    def tearDown(self):
        executor = MigrationExecutor(connection)
        executor.migrate(executor.loader.graph.leaf_nodes())
        super().tearDown()

    def test_fresh_schema_has_no_mediahub_residue(self):
        self.assertNotIn("mediahub_mediaasset", connection.introspection.table_names())
        self.assertFalse(ContentType.objects.filter(app_label="mediahub").exists())

    def test_cleanup_removes_legacy_table_content_type_and_permissions(self):
        executor = MigrationExecutor(connection)
        executor.migrate(self.migrate_from)
        content_type = ContentType.objects.create(app_label="mediahub", model="mediaasset")
        Permission.objects.create(
            content_type=content_type,
            codename="view_mediaasset",
            name="Can view media asset",
        )
        with connection.cursor() as cursor:
            cursor.execute("CREATE TABLE mediahub_mediaasset (id integer primary key)")

        MigrationExecutor(connection).migrate(self.migrate_to)

        self.assertNotIn("mediahub_mediaasset", connection.introspection.table_names())
        self.assertFalse(ContentType.objects.filter(app_label="mediahub").exists())
        self.assertFalse(Permission.objects.filter(content_type_id=content_type.pk).exists())

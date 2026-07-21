import os
from pathlib import Path, PurePosixPath

from django.apps import apps
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db.models import FileField


class Command(BaseCommand):
    help = "Inventaria arquivos órfãos no MEDIA_ROOT e, opcionalmente, os exclui."

    def add_arguments(self, parser):
        parser.add_argument(
            "--delete",
            action="store_true",
            help="Exclui permanentemente os arquivos órfãos encontrados.",
        )
        parser.add_argument(
            "--confirm-root",
            help=(
                "Confirma o caminho absoluto de um MEDIA_ROOT personalizado. "
                "Obrigatório com --delete fora de BASE_DIR/media."
            ),
        )

    def handle(self, *args, **options):
        configured_root = str(settings.MEDIA_ROOT).strip()
        if not configured_root:
            raise CommandError("MEDIA_ROOT deve apontar para um diretório dedicado.")

        media_root = Path(configured_root).resolve()
        base_dir = Path(settings.BASE_DIR).resolve()
        protected_roots = {
            Path(media_root.anchor),
            Path.home().resolve(),
            base_dir,
            base_dir.parent,
        }
        if media_root in protected_roots:
            raise CommandError("MEDIA_ROOT deve apontar para um diretório dedicado.")
        if media_root.exists() and not media_root.is_dir():
            raise CommandError(f"MEDIA_ROOT não é um diretório: {media_root}")
        if options["delete"] and media_root != (base_dir / "media").resolve():
            confirmed_root = options.get("confirm_root")
            if not confirmed_root or Path(confirmed_root).expanduser().resolve() != media_root:
                raise CommandError(
                    "Para excluir em um MEDIA_ROOT personalizado, repita o caminho absoluto "
                    f"com --confirm-root={media_root}."
                )

        referenced = self._referenced_files()
        stored = self._stored_files(media_root)
        orphaned = sorted(stored - referenced)
        missing = sorted(referenced - stored)

        self.stdout.write(f"MEDIA_ROOT: {media_root}")
        self.stdout.write(f"Arquivos encontrados: {len(stored)}")
        self.stdout.write(f"Arquivos referenciados: {len(referenced)}")
        self.stdout.write(f"Arquivos órfãos: {len(orphaned)}")
        self._write_list("Órfãos", orphaned)
        self.stdout.write(f"Referências sem arquivo: {len(missing)}")
        self._write_list("Ausentes", missing)

        if not options["delete"]:
            self.stdout.write("Dry-run: nenhum arquivo foi removido. Use --delete para excluir os órfãos.")
            return

        removed = 0
        for relative_name in orphaned:
            target = media_root.joinpath(*PurePosixPath(relative_name).parts)
            try:
                target.unlink()
            except FileNotFoundError:
                continue
            removed += 1
        self.stdout.write(self.style.SUCCESS(f"Arquivos removidos: {removed}"))

    @staticmethod
    def _referenced_files():
        referenced = set()
        for model in apps.get_models():
            for field in model._meta.concrete_fields:
                if not isinstance(field, FileField):
                    continue
                values = model._base_manager.values_list(field.attname, flat=True).iterator()
                for value in values:
                    if not value:
                        continue
                    name = PurePosixPath(str(value).replace("\\", "/"))
                    referenced.add(name.as_posix())
        return referenced

    @staticmethod
    def _stored_files(media_root):
        if not media_root.exists():
            return set()

        stored = set()
        for directory, _, filenames in os.walk(media_root, followlinks=False):
            directory = Path(directory)
            for filename in filenames:
                stored.add((directory / filename).relative_to(media_root).as_posix())
        return stored

    def _write_list(self, label, paths):
        if not paths:
            return
        self.stdout.write(f"{label}:")
        for path in paths:
            self.stdout.write(f"- {path}")

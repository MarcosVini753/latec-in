from django.core.management.base import BaseCommand
from django.utils.text import slugify

from apps.axes.models import ResearchAxis
from apps.core.models import SiteSettings
from apps.learning.models import LearningTrack
from apps.metrics.models import ImpactMetric
from apps.news.models import PostCategory
from apps.people.models import Role
from apps.portfolio.models import ProjectCategory, ProjectStatus


class Command(BaseCommand):
    help = "Cria dados iniciais idempotentes para desenvolvimento e homologação."

    def handle(self, *args, **options):
        self.seed_roles()
        self.seed_axes()
        self.seed_project_categories()
        self.seed_project_statuses()
        self.seed_post_categories()
        self.seed_learning_tracks()
        self.seed_metrics()
        self.seed_site_settings()
        self.stdout.write(self.style.SUCCESS("Seed inicial concluído."))

    def seed_roles(self):
        roles = [
            ("Coordenadora", "Responsável pela coordenação institucional e publicação final."),
            ("Professor", "Docente, orientador ou mentor vinculado à LATEC.IN."),
            ("Ligante", "Membro discente da liga acadêmica."),
            ("Pesquisador", "Pessoa vinculada à pesquisa e produção científica."),
            ("Estagiário", "Pessoa em estágio ou colaboração formativa."),
            ("Colaborador", "Colaborador externo ou institucional."),
            ("Egresso", "Pessoa que já integrou a LATEC.IN."),
        ]
        for order, (name, description) in enumerate(roles, start=1):
            Role.objects.update_or_create(
                slug=slugify(name),
                defaults={"name": name, "description": description, "is_active": True, "display_order": order},
            )

    def seed_axes(self):
        axes = [
            (
                1,
                "Etnobotânica e Pós-Colheita",
                "Cultivo, manejo e óleos essenciais.",
                "etnobotânica,pós-colheita,óleos essenciais",
            ),
            (
                2,
                "Práticas em Laboratório e Nanotecnologia",
                "Farmácia Viva, farmacologia aplicada a plantas medicinais e fitoquímica.",
                "laboratório,nanotecnologia,fitoquímica,farmácia viva",
            ),
            (
                3,
                "Nutrição e Ciências dos Alimentos",
                "Educação alimentar, desenvolvimento e avaliação de alimentos.",
                "nutrição,ciências dos alimentos,educação alimentar",
            ),
            (
                4,
                "Saúde e bem-estar",
                "Produção de ativos para aplicação em saúde integrativa.",
                "saúde,bem-estar,saúde integrativa",
            ),
            (
                5,
                "Produção Vegetal e Biotecnologia",
                "Produção vegetal, biotecnologia de plantas, fitotecnia, genética vegetal, horticultura, manejo de culturas e PANCs.",
                "produção vegetal,biotecnologia,fitotecnia,genética vegetal,pancs",
            ),
            (
                6,
                "Agroindustrialização",
                "Desenvolvimento de produtos, processamento de matérias-primas amazônicas e inovação tecnológica.",
                "agroindustrialização,produtos amazônicos,inovação tecnológica",
            ),
            (
                7,
                "Redação Científica",
                "Produção acadêmica, escrita de artigos, resumos, projetos e revisão de literatura.",
                "redação científica,artigos,resumos,revisão de literatura",
            ),
        ]
        for number, title, description, keywords in axes:
            ResearchAxis.objects.update_or_create(
                number=number,
                defaults={
                    "title": title,
                    "slug": slugify(title),
                    "description": description,
                    "keywords": keywords,
                    "is_active": True,
                    "display_order": number,
                },
            )

        # TODO: validar grafia dos nomes dos mentores antes de popular pessoas e mentorias reais.

    def seed_project_categories(self):
        categories = ["Ensino", "Pesquisa", "Extensão", "Produção Científica", "Startup", "Premiação"]
        for order, name in enumerate(categories, start=1):
            ProjectCategory.objects.update_or_create(
                slug=slugify(name),
                defaults={"name": name, "is_active": True, "display_order": order},
            )

    def seed_project_statuses(self):
        statuses = ["Planejado", "Em andamento", "Concluído", "Arquivado"]
        for order, name in enumerate(statuses, start=1):
            ProjectStatus.objects.update_or_create(
                slug=slugify(name),
                defaults={"name": name, "display_order": order},
            )

    def seed_post_categories(self):
        categories = ["Notícia", "Blog", "Jornal", "Evento", "Premiação", "Artigo técnico", "Comunicado"]
        for order, name in enumerate(categories, start=1):
            PostCategory.objects.update_or_create(
                slug=slugify(name),
                defaults={"name": name, "is_active": True, "display_order": order},
            )

    def seed_learning_tracks(self):
        tracks = ["Cursos e oficinas", "Workshops", "Simpósios e palestras", "Materiais abertos"]
        for order, title in enumerate(tracks, start=1):
            LearningTrack.objects.update_or_create(
                slug=slugify(title),
                defaults={"title": title, "is_active": True, "display_order": order},
            )

    def seed_metrics(self):
        metrics = [
            ("membros", "Membros", 0),
            ("projetos", "Projetos", 0),
            ("publicacoes", "Artigos e publicações", 0),
            ("parcerias", "Parcerias", 0),
            ("cursos", "Cursos", 0),
            ("eventos", "Eventos", 0),
            ("premiacoes", "Premiações", 0),
        ]
        for order, (key, label, value) in enumerate(metrics, start=1):
            ImpactMetric.objects.update_or_create(
                key=key,
                defaults={"label": label, "value": value, "is_active": True, "display_order": order},
            )

    def seed_site_settings(self):
        SiteSettings.objects.update_or_create(
            site_name="LATEC.IN",
            defaults={
                "description": "Liga Acadêmica de Biotecnologia, Biodiversidade e Inovação.",
                "institution": "LATEC.IN",
                "is_active": True,
            },
        )

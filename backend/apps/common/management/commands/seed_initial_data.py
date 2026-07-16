from datetime import date, datetime, time
from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.text import slugify

from apps.axes.models import AxisMentorship, ResearchAxis
from apps.common.models import EditorialStatus
from apps.core.models import HeroBanner, InstitutionalSection, SiteSettings
from apps.institutional.models import InstitutionalUnit
from apps.learning.models import Course, CourseMaterial, LearningTrack
from apps.metrics.models import ImpactMetric
from apps.news.models import Post, PostCategory
from apps.people.models import Person, Role
from apps.portfolio.models import Project, ProjectCategory, ProjectLink, ProjectResult, ProjectStatus, ProjectTeamMember


PEOPLE = [
    (1, "Marta Adelino", "Coordenadora", "Professora doutora e coordenadora da LATEC.IN, com larga experiência em biotecnologia e gestão de projetos.", "js/pics/marta.png"),
    (2, "Gabriel Daniel", "Estagiário", "Estudante de Sistemas de Informação na UFAC, responsável pela criação deste protótipo.", "js/pics/gabriel.png"),
    (3, "Ana Souza", "Pesquisadora", "Discente pesquisadora focada em bioinformática e biodiversidade amazônica.", "js/pics/ana.png"),
    (4, "Marcos Moraes", "Ligante", "Estudante de Sistemas de Informação na UFAC, responsável pela criação deste protótipo.", "js/pics/marcos.png"),
    (5, "Kleyton Passos", "Professor", "Dr. em Ciências da Saúde", "js/pics/kleyton.png"),
    (6, "Luciana Castello", "Professor", "Engenheira de alimentos e Dra. em Ciência de Alimentos", "js/pics/luciana.png"),
    (7, "Bruno Favero", "Professor", "Engenheiro Agronômico e Dr. em Botânica", "js/pics/bruno.png"),
    (8, "Dayam Marques", "Professor", "Farmacêutico e Mestre em Quimica", "js/pics/dayam.png"),
    (9, "Anne Grace", "Professor", "Enfermeira, Mestre em Educação e Tecnologias de Enfermagem", "js/pics/anne.png"),
    (10, "Almecina Balbino", "Professor", "Engenheira Agrônoma e Dra. em Horticultura", "js/pics/almecina.png"),
    (11, "Marilene Lima", "Professor", "Engenheira Agrônoma e Dra. em Fitotecnia", "js/pics/marilene.png"),
    (12, "Bruna Viana", "Professor", "Nutricionista, Dra. em sanidade e produção animal sustentável na Amazônia Ocidental", "js/pics/bruna.png"),
    (13, "Adson Jhonnata Lima Ferreira", "Ligante", "", "js/pics/Adson Jhonnata Lima Ferreira.jpeg"),
    (14, "Ana Clara Souza", "Ligante", "", "js/pics/Ana Clara Souza.jpeg"),
    (15, "Ana Vivyan Ferreira Cavalcante", "Ligante", "", "js/pics/Ana Vivyan Ferreira Cavalcante.jpeg"),
    (16, "Andrick Alexandre de Oliveira", "Ligante", "", "js/pics/Andrick Alexandre de Oliveira.jpeg"),
    (17, "Bruno Carvalho dos Santos", "Ligante", "", "js/pics/Bruno Carvalho dos Santos.jpeg"),
    (18, "Cristielen Frota", "Ligante", "", "js/pics/Cristielen Frota.jpeg"),
    (19, "Débora Rocha de Mesquita", "Ligante", "", "js/pics/Débora Rocha de Mesquita.jpeg"),
    (20, "Deborah da Silva Lima", "Ligante", "", "js/pics/Deborah da Silva Lima.jpeg"),
    (21, "Eduardo dos Santos Feitosa", "Ligante", "", "js/pics/Eduardo dos Santos Feitosa.jpeg"),
    (22, "Eshyla Maria da Silva Maia", "Ligante", "", "js/pics/Eshyla Maria da Silva Maia.jpeg"),
    (23, "Felipe Gabriel Dantas Azevedo", "Ligante", "", "js/pics/Felipe Gabriel Dantas Azevedo.jpeg"),
    (24, "Laíza Rivera de Sousa", "Ligante", "", "js/pics/Laíza Rivera de Sousa.jpeg"),
    (25, "Lougan Coelho Alves", "Ligante", "", "js/pics/Lougan Coelho Alves.jpeg"),
    (26, "Mary Anny Mariscal", "Ligante", "", "js/pics/Mary Anny Mariscal.jpeg"),
    (27, "Mirela Brito", "Ligante", "", "js/pics/Mirela Brito.jpeg"),
    (28, "Sabrina Brasil de Oliveira", "Ligante", "", "js/pics/Sabrina Brasil de Oliveira.jpeg"),
    (29, "Salvino de Castro", "Ligante", "", "js/pics/Salvino de Castro.jpeg"),
    (30, "Stéphany Portela", "Ligante", "", "js/pics/Stéphany Portela.jpeg"),
    (31, "Suzanne Hadassa Da Silva Lima", "Ligante", "", "js/pics/Suzanne Hadassa Da Silva Lima.jpeg"),
    (32, "Thais Cristina Silva Filgueira Monteiro", "Ligante", "", "js/pics/Thais Cristina Silva Filgueira Monteiro.jpeg"),
    (33, "Thiago Schuster Casas", "Ligante", "", "js/pics/Thiago Schuster Casas.jpeg"),
]

PROJECTS = [
    {
        "source_id": 1,
        "title": "Fábrica de Ensino: Bootcamp de Startups",
        "category": "Ensino",
        "area": "Fábrica de Ensino",
        "status": "Concluído",
        "year": 2025,
        "summary": "Bootcamp intensivo de Startups para novos membros da LATEC.IN.",
        "problem": "Falta de capacitação em desenvolvimento de negócios entre os integrantes.",
        "solution": "Proporcionar um treinamento prático e imersivo em desenvolvimento de startups.",
        "results": ["Relatório de atividades", "Apostila digital"],
        "team": [1, 2, 3],
        "link": "",
    },
    {
        "source_id": 2,
        "title": "Pesquisa de Bioativos da Amazônia",
        "category": "Pesquisa",
        "area": "Projetos de Pesquisa",
        "status": "Em andamento",
        "year": 2026,
        "summary": "Estudo dos compostos bioativos presentes em espécies amazônicas.",
        "problem": "Necessidade de explorar novos fármacos e compostos naturais.",
        "solution": "Investigar propriedades bioativas de plantas da região amazônica.",
        "results": ["Artigo científico", "Protótipo de extrato"],
        "team": [1, 3],
        "link": "",
    },
    {
        "source_id": 3,
        "title": "Extensão em Tecnologias Sustentáveis",
        "category": "Extensão",
        "area": "Extensão Tecnológica",
        "status": "Planejado",
        "year": 2026,
        "summary": "Iniciativa para aplicar tecnologia verde em comunidades locais.",
        "problem": "Falta de acesso a tecnologias sustentáveis em regiões remotas.",
        "solution": "Desenvolver protótipos de baixo custo e treinamentos comunitários.",
        "results": ["Manual de boas práticas"],
        "team": [2, 3],
        "link": "",
    },
]

POSTS = [
    {
        "title": "Coordenadora do LATEC.IN é premiada por inovação tecnológica",
        "date": "2026-05-29",
        "summary": "A professora Marta Adelino recebeu o prêmio de inovação tecnológica da UFAC por seu trabalho à frente da LATEC.IN.",
        "content": "A coordenadora da LATEC.IN, professora Marta Adelino, foi reconhecida com o prêmio de inovação tecnológica da Universidade Federal do Acre (UFAC) em 2026. O prêmio destaca sua liderança e os resultados alcançados pela liga em projetos de ensino, pesquisa e extensão. A cerimônia de premiação ocorreu no auditório central da UFAC, onde Marta recebeu um certificado e um troféu em reconhecimento ao seu trabalho inovador.",
        "image": "js/pics/certificado.png",
    },
    {
        "title": "LATEC.IN participa do congresso nacional de inovação",
        "date": "2026-05-15",
        "summary": "A LATEC.IN apresentou três projetos no congresso nacional, recebendo destaque na sessão de biotecnologia.",
        "content": "No congresso nacional de inovação tecnológica, a LATEC.IN foi representada pelos projetos “Fábrica de Ensino”, “Pesquisa de Bioativos da Amazônia” e “Extensão em Tecnologias Sustentáveis”. As apresentações foram bem recebidas e destacaram o potencial dos alunos da UFAC.",
        "image": "",
    },
]

COURSES = [
    {
        "title": "Nanotecnologias de cosméticos",
        "description": "Aprenda sobre as aplicações de nanotecnologia na indústria cosmética.",
        "date": "2026-07-10",
        "enrollment_status": Course.EnrollmentStatus.OPEN,
        "materials": ["Apostila Nanotecnologia.pdf"],
        "link": "",
    },
    {
        "title": "Workshop de ML em Biotecnologia",
        "description": "Fundamentos de IA e Machine Learning aplicados à biotecnologia.",
        "date": "2026-08-15",
        "enrollment_status": Course.EnrollmentStatus.COMING_SOON,
        "materials": [],
        "link": "",
    },
]

MATERIALS = {
    "Apostila Nanotecnologia.pdf": {
        "title": "Apostila de Nanotecnologia",
        "description": "Apostila utilizada no curso de Nanotecnologia da LATEC.IN.",
        "file": "assets/images/apostila-nanotecnologia.pdf",
    }
}

ROLE_ALIASES = {
    "Pesquisadora": "pesquisador",
}


class Command(BaseCommand):
    help = "Cria dados iniciais idempotentes para desenvolvimento e homologação."

    def handle(self, *args, **options):
        self.person_by_source_id = {}
        self.seed_institutional_units()
        self.seed_roles()
        self.seed_people()
        self.seed_axes()
        self.seed_axis_mentorships()
        self.seed_project_categories()
        self.seed_project_statuses()
        self.seed_projects()
        self.seed_post_categories()
        self.seed_posts()
        self.seed_learning_tracks()
        self.seed_courses()
        self.seed_metrics()
        self.seed_site_settings()
        self.stdout.write(self.style.SUCCESS("Seed inicial concluído."))

    def seed_institutional_units(self):
        self.labtec_unit, _created = InstitutionalUnit.objects.update_or_create(
            slug="labtec-in",
            defaults={
                "name": "LABTEC.IN",
                "acronym": "LABTEC.IN",
                "unit_type": InstitutionalUnit.UnitType.LABORATORY,
                "parent": None,
                "description": "Laboratório de Biotecnologia, Biodiversidade e Inovação.",
                "is_active": True,
                "is_public": True,
                "display_order": 1,
            },
        )
        self.latec_unit, _created = InstitutionalUnit.objects.update_or_create(
            slug="latec",
            defaults={
                "name": "LATEC",
                "acronym": "LATEC",
                "unit_type": InstitutionalUnit.UnitType.ACADEMIC_LEAGUE,
                "parent": self.labtec_unit,
                "description": "Liga acadêmica vinculada ao LABTEC.IN.",
                "is_active": True,
                "is_public": True,
                "display_order": 2,
            },
        )

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

    def seed_people(self):
        for order, (source_id, name, role_name, bio, photo_path) in enumerate(PEOPLE, start=1):
            role = Role.objects.get(slug=ROLE_ALIASES.get(role_name, slugify(role_name)))
            person, _created = Person.objects.update_or_create(
                slug=slugify(name),
                defaults={
                    "full_name": name,
                    "role": role,
                    "short_bio": bio,
                    "is_active": True,
                    "is_featured": source_id <= 12,
                    "display_order": order,
                },
            )
            self.attach_local_file(person, "photo", photo_path)
            self.person_by_source_id[source_id] = person

    def seed_axes(self):
        axes = [
            (1, "Etnobotânica e Pós-Colheita", "Cultivo, manejo e óleos essenciais.", "etnobotânica,pós-colheita,óleos essenciais"),
            (2, "Práticas em Laboratório e Nanotecnologia", "Farmácia Viva, farmacologia aplicada a plantas medicinais e fitoquímica.", "laboratório,nanotecnologia,fitoquímica,farmácia viva"),
            (3, "Nutrição e Ciências dos Alimentos", "Educação alimentar, desenvolvimento e avaliação de alimentos.", "nutrição,ciências dos alimentos,educação alimentar"),
            (4, "Saúde e bem-estar", "Produção de ativos para aplicação em saúde integrativa.", "saúde,bem-estar,saúde integrativa"),
            (5, "Produção Vegetal e Biotecnologia", "Produção vegetal, biotecnologia de plantas, fitotecnia, genética vegetal, horticultura, manejo de culturas e PANCs.", "produção vegetal,biotecnologia,fitotecnia,genética vegetal,pancs"),
            (6, "Agroindustrialização", "Desenvolvimento de produtos, processamento de matérias-primas amazônicas e inovação tecnológica.", "agroindustrialização,produtos amazônicos,inovação tecnológica"),
            (7, "Redação Científica", "Produção acadêmica, escrita de artigos, resumos, projetos e revisão de literatura.", "redação científica,artigos,resumos,revisão de literatura"),
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

    def seed_axis_mentorships(self):
        mentorships = [
            (1, "Almecina Balbino"),
            (2, "Marta Adelino"),
            (3, "Bruna Viana"),
            (4, "Kleyton Passos"),
            (5, "Marilene Lima"),
            (5, "Bruno Favero"),
            (6, "Luciana Castello"),
            (7, "Dayam Marques"),
            (7, "Anne Grace"),
        ]
        for order, (axis_number, person_name) in enumerate(mentorships, start=1):
            axis = ResearchAxis.objects.get(number=axis_number)
            person = Person.objects.filter(slug=slugify(person_name)).first()
            if not person:
                continue
            AxisMentorship.objects.update_or_create(
                axis=axis,
                person=person,
                defaults={"role": "Mentor", "is_main_mentor": True, "display_order": order},
            )

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

    def seed_projects(self):
        for order, item in enumerate(PROJECTS, start=1):
            project, _created = Project.objects.update_or_create(
                slug=slugify(item["title"]),
                defaults={
                    "title": item["title"],
                    "category": ProjectCategory.objects.get(slug=slugify(item["category"])),
                    "area": item["area"],
                    "status": ProjectStatus.objects.get(slug=slugify(item["status"])),
                    "year": item["year"],
                    "summary": item["summary"],
                    "problem": item["problem"],
                    "solution": item["solution"],
                    "editorial_status": EditorialStatus.PUBLISHED,
                    "is_published": True,
                    "published_at": self.datetime_from_date(date(item["year"], 1, 1)),
                    "is_featured": order <= 2,
                    "display_order": order,
                },
            )
            for result_order, result_title in enumerate(item["results"], start=1):
                ProjectResult.objects.update_or_create(
                    project=project,
                    title=result_title,
                    defaults={"description": "", "display_order": result_order},
                )
            for member_order, source_id in enumerate(item["team"], start=1):
                person = self.person_by_source_id.get(source_id) or Person.objects.filter(slug=slugify(dict((p[0], p[1]) for p in PEOPLE).get(source_id, ""))).first()
                if not person:
                    continue
                ProjectTeamMember.objects.update_or_create(
                    project=project,
                    person=person,
                    defaults={"role": "Equipe", "is_lead": member_order == 1, "display_order": member_order},
                )
            if item["link"]:
                ProjectLink.objects.update_or_create(
                    project=project,
                    url=item["link"],
                    defaults={"label": "Link externo", "link_type": "externo", "display_order": 1},
                )

    def seed_post_categories(self):
        categories = ["Notícia", "Blog", "Jornal", "Evento", "Premiação", "Artigo técnico", "Comunicado"]
        for order, name in enumerate(categories, start=1):
            PostCategory.objects.update_or_create(
                slug=slugify(name),
                defaults={"name": name, "is_active": True, "display_order": order},
            )

    def seed_posts(self):
        category = PostCategory.objects.get(slug=slugify("Notícia"))
        for order, item in enumerate(POSTS, start=1):
            published_at = self.datetime_from_iso_date(item["date"])
            post, _created = Post.objects.update_or_create(
                slug=slugify(item["title"]),
                defaults={
                    "title": item["title"],
                    "category": category,
                    "summary": item["summary"],
                    "content": item["content"],
                    "status": EditorialStatus.PUBLISHED,
                    "is_published": True,
                    "published_at": published_at,
                    "is_featured": order <= 2,
                    "display_order": order,
                },
            )
            self.attach_local_file(post, "cover_image", item["image"])

    def seed_learning_tracks(self):
        tracks = ["Cursos e oficinas", "Workshops", "Simpósios e palestras", "Materiais abertos"]
        for order, title in enumerate(tracks, start=1):
            LearningTrack.objects.update_or_create(
                slug=slugify(title),
                defaults={"title": title, "is_active": True, "display_order": order},
            )

    def seed_courses(self):
        track = LearningTrack.objects.get(slug=slugify("Cursos e oficinas"))
        for order, item in enumerate(COURSES, start=1):
            course, _created = Course.objects.update_or_create(
                slug=slugify(item["title"]),
                defaults={
                    "title": item["title"],
                    "track": track,
                    "description": item["description"],
                    "start_date": date.fromisoformat(item["date"]),
                    "enrollment_status": item["enrollment_status"],
                    "registration_url": item["link"],
                    "editorial_status": EditorialStatus.PUBLISHED,
                    "is_published": True,
                    "published_at": self.datetime_from_iso_date(item["date"]),
                    "is_featured": order == 1,
                    "display_order": order,
                },
            )
            for material_order, material_name in enumerate(item["materials"], start=1):
                material_data = MATERIALS.get(material_name, {"title": material_name, "description": "", "file": ""})
                material, _created = CourseMaterial.objects.update_or_create(
                    course=course,
                    title=material_data["title"],
                    defaults={
                        "description": material_data["description"],
                        "is_public": True,
                        "display_order": material_order,
                    },
                )
                self.attach_local_file(material, "file", material_data["file"])

    def seed_metrics(self):
        metrics = [
            ("membros", "Membros", 33),
            ("projetos", "Projetos", 20),
            ("publicacoes", "Artigos e publicações", 12),
            ("parcerias", "Parcerias", 5),
            ("cursos", "Cursos", 2),
            ("eventos", "Eventos", 0),
            ("premiacoes", "Premiações", 1),
        ]
        for order, (key, label, value) in enumerate(metrics, start=1):
            ImpactMetric.objects.update_or_create(
                key=key,
                defaults={"label": label, "value": value, "is_active": True, "display_order": order},
            )

    def seed_site_settings(self):
        site_settings = (
            SiteSettings.objects.filter(unit=self.labtec_unit).order_by("id").first()
            or SiteSettings.objects.filter(site_name__in=("LABTEC.IN", "LATEC.IN")).order_by("id").first()
            or SiteSettings()
        )
        site_settings.unit = self.labtec_unit
        site_settings.site_name = "LABTEC.IN"
        site_settings.institution = "Laboratório de Biotecnologia, Biodiversidade e Inovação"
        site_settings.is_active = True
        if (
            not site_settings.description
            or site_settings.description == "Liga Acadêmica de Biotecnologia, Biodiversidade e Inovação."
        ):
            site_settings.description = "Portal institucional do LABTEC.IN."
        site_settings.save()

        HeroBanner.objects.update_or_create(
            title="Biotecnologia, biodiversidade e inovação",
            defaults={
                "unit": self.labtec_unit,
                "subtitle": "Uma liga acadêmica conectando ensino, pesquisa e extensão para transformar ciência em soluções para a Amazônia.",
                "cta_label": "Conheça os projetos",
                "cta_url": "#portfolio",
                "is_published": True,
                "display_order": 1,
            },
        )
        sections = [
            ("mission", "Missão", "Desenvolver soluções tecnológicas e científicas para a Amazônia, promovendo formação acadêmica e impacto social."),
            ("vision", "Visão", "Tornar-se referência nacional em inovação biotecnológica e proteção da biodiversidade amazônica."),
            ("values", "Valores", "Ética, inovação, sustentabilidade, colaboração e excelência."),
        ]
        for order, (section_type, title, content) in enumerate(sections, start=1):
            InstitutionalSection.objects.update_or_create(
                slug=slugify(title),
                defaults={
                    "unit": self.labtec_unit,
                    "section_type": section_type,
                    "title": title,
                    "content": content,
                    "is_published": True,
                    "display_order": order,
                },
            )

    def attach_local_file(self, instance, field_name, source_relative_path):
        if not source_relative_path or source_relative_path.startswith(("http://", "https://")):
            return
        source_path = Path(settings.BASE_DIR).parent / source_relative_path
        if not source_path.exists():
            return

        field_file = getattr(instance, field_name)
        if field_file.name and default_storage.exists(field_file.name):
            return

        model_field = instance._meta.get_field(field_name)
        generated_name = model_field.generate_filename(instance, source_path.name)
        if default_storage.exists(generated_name):
            setattr(instance, field_name, generated_name)
            instance.save(update_fields=[field_name])
            return

        with source_path.open("rb") as file_obj:
            field_file.save(source_path.name, File(file_obj), save=True)

    def datetime_from_iso_date(self, value):
        return self.datetime_from_date(date.fromisoformat(value))

    def datetime_from_date(self, value):
        return timezone.make_aware(datetime.combine(value, time.min))

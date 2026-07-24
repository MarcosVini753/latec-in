from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import F, Q

from apps.common.models import BaseModel, EditorialStatus


class ResearchProject(BaseModel):
    class ProjectStatus(models.TextChoices):
        PLANNED = "planned", "Planejada"
        IN_PROGRESS = "in_progress", "Em andamento"
        COMPLETED = "completed", "Concluída"
        SUSPENDED = "suspended", "Suspensa"
        CANCELED = "canceled", "Cancelada"

    unit = models.ForeignKey(
        "institutional.InstitutionalUnit",
        on_delete=models.PROTECT,
        related_name="research_projects",
    )
    axis = models.ForeignKey(
        "axes.ResearchAxis",
        on_delete=models.SET_NULL,
        related_name="research_projects",
        blank=True,
        null=True,
    )
    title = models.CharField(max_length=220)
    slug = models.SlugField(max_length=240, unique=True)
    summary = models.TextField(blank=True)
    file = models.FileField(upload_to="research/projects/", blank=True)
    external_url = models.URLField(blank=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    project_status = models.CharField(
        max_length=32,
        choices=ProjectStatus.choices,
        default=ProjectStatus.PLANNED,
    )
    editorial_status = models.CharField(
        max_length=32,
        choices=EditorialStatus.choices,
        default=EditorialStatus.DRAFT,
    )
    published_at = models.DateTimeField(blank=True, null=True)
    include_in_parent_ecosystem = models.BooleanField(
        default=False,
        help_text="Inclui este conteúdo no recorte público da unidade mãe.",
    )
    team = models.ManyToManyField(
        "people.Person",
        through="ResearchProjectMember",
        related_name="research_projects",
        blank=True,
    )

    class Meta:
        ordering = ("-start_date", "title")
        constraints = [
            models.CheckConstraint(
                check=Q(end_date__isnull=True) | Q(start_date__isnull=True) | Q(end_date__gte=F("start_date")),
                name="research_project_valid_date_range",
            ),
        ]
        verbose_name = "pesquisa"
        verbose_name_plural = "pesquisas"

    def clean(self):
        super().clean()
        if self.start_date and self.end_date and self.end_date < self.start_date:
            raise ValidationError({"end_date": "A data final deve ser igual ou posterior à data inicial."})

    def __str__(self) -> str:
        return self.title


class ResearchProjectMember(BaseModel):
    class Role(models.TextChoices):
        COORDINATOR = "coordinator", "Coordenador"
        RESEARCHER = "researcher", "Pesquisador"
        ADVISOR = "advisor", "Orientador"
        SCHOLARSHIP_HOLDER = "scholarship_holder", "Bolsista"
        VOLUNTEER = "volunteer", "Voluntário"
        COLLABORATOR = "collaborator", "Colaborador"

    research_project = models.ForeignKey(
        ResearchProject,
        on_delete=models.CASCADE,
        related_name="team_members",
    )
    person = models.ForeignKey(
        "people.Person",
        on_delete=models.CASCADE,
        related_name="research_project_memberships",
    )
    role = models.CharField(max_length=32, choices=Role.choices, default=Role.COLLABORATOR)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("display_order", "person__full_name")
        constraints = [
            models.UniqueConstraint(
                fields=("research_project", "person"),
                name="unique_research_project_member",
            ),
        ]
        verbose_name = "membro de pesquisa"
        verbose_name_plural = "membros de pesquisa"

    def __str__(self) -> str:
        return f"{self.person} em {self.research_project}"


class AcademicWork(BaseModel):
    class WorkType(models.TextChoices):
        TCC = "tcc", "TCC"
        MONOGRAPH = "monograph", "Monografia"
        SCIENTIFIC_INITIATION = "scientific_initiation", "Iniciação científica"
        DISSERTATION = "dissertation", "Dissertação"
        THESIS = "thesis", "Tese"
        OTHER = "other", "Outro"

    unit = models.ForeignKey(
        "institutional.InstitutionalUnit",
        on_delete=models.PROTECT,
        related_name="academic_works",
    )
    research_project = models.ForeignKey(
        ResearchProject,
        on_delete=models.SET_NULL,
        related_name="academic_works",
        blank=True,
        null=True,
    )
    title = models.CharField(max_length=220)
    slug = models.SlugField(max_length=240, unique=True)
    work_type = models.CharField(max_length=32, choices=WorkType.choices)
    course = models.CharField(max_length=180, blank=True)
    institution = models.CharField(max_length=220, blank=True)
    year = models.PositiveSmallIntegerField(blank=True, null=True)
    abstract = models.TextField(blank=True)
    keywords = models.TextField(blank=True, help_text="Palavras-chave separadas por vírgula.")
    file = models.FileField(upload_to="research/academic-works/", blank=True)
    external_url = models.URLField(blank=True)
    editorial_status = models.CharField(
        max_length=32,
        choices=EditorialStatus.choices,
        default=EditorialStatus.DRAFT,
    )
    published_at = models.DateTimeField(blank=True, null=True)
    include_in_parent_ecosystem = models.BooleanField(
        default=False,
        help_text="Inclui este conteúdo no recorte público da unidade mãe.",
    )
    contributors = models.ManyToManyField(
        "people.Person",
        through="AcademicWorkContributor",
        related_name="academic_works",
        blank=True,
    )

    class Meta:
        ordering = ("-year", "title")
        verbose_name = "trabalho acadêmico"
        verbose_name_plural = "trabalhos acadêmicos"

    def __str__(self) -> str:
        return self.title


class AcademicWorkContributor(BaseModel):
    class Role(models.TextChoices):
        AUTHOR = "author", "Autor"
        ADVISOR = "advisor", "Orientador"
        CO_ADVISOR = "co_advisor", "Coorientador"
        EXAMINER = "examiner", "Avaliador"
        COLLABORATOR = "collaborator", "Colaborador"

    academic_work = models.ForeignKey(
        AcademicWork,
        on_delete=models.CASCADE,
        related_name="work_contributors",
    )
    person = models.ForeignKey(
        "people.Person",
        on_delete=models.CASCADE,
        related_name="academic_work_contributions",
    )
    role = models.CharField(max_length=32, choices=Role.choices)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("display_order", "person__full_name")
        constraints = [
            models.UniqueConstraint(
                fields=("academic_work", "person", "role"),
                name="unique_academic_work_contributor",
            ),
        ]
        verbose_name = "colaborador de trabalho acadêmico"
        verbose_name_plural = "colaboradores de trabalhos acadêmicos"

    def __str__(self) -> str:
        return f"{self.person} em {self.academic_work}"

from django.db import models

from apps.common.models import BaseModel


class InstitutionalUnit(BaseModel):
    class UnitType(models.TextChoices):
        LABORATORY = "laboratory", "Laboratório"
        ACADEMIC_LEAGUE = "academic_league", "Liga acadêmica"
        PROGRAM = "program", "Programa"
        RESEARCH_GROUP = "research_group", "Grupo de pesquisa"
        INITIATIVE = "initiative", "Iniciativa"

    name = models.CharField(max_length=180)
    acronym = models.CharField(max_length=40)
    slug = models.SlugField(max_length=200, unique=True)
    unit_type = models.CharField(max_length=40, choices=UnitType.choices)
    parent = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        related_name="children",
        blank=True,
        null=True,
    )
    description = models.TextField(blank=True)
    mission = models.TextField(blank=True)
    vision = models.TextField(blank=True)
    logo = models.ImageField(upload_to="institutional/logos/", blank=True)
    cover_image = models.ImageField(upload_to="institutional/covers/", blank=True)
    contact_email = models.EmailField(blank=True)
    website_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    is_public = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("display_order", "name")
        verbose_name = "unidade institucional"
        verbose_name_plural = "unidades institucionais"

    def __str__(self) -> str:
        return self.acronym or self.name


class InstitutionMembership(BaseModel):
    person = models.ForeignKey(
        "people.Person",
        on_delete=models.CASCADE,
        related_name="institution_memberships",
    )
    unit = models.ForeignKey(
        InstitutionalUnit,
        on_delete=models.CASCADE,
        related_name="memberships",
    )
    role = models.CharField(max_length=120)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_public = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("unit__display_order", "display_order", "person__full_name", "role")
        verbose_name = "vínculo institucional"
        verbose_name_plural = "vínculos institucionais"

    def __str__(self) -> str:
        return f"{self.person} — {self.role} em {self.unit}"

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import F, Q

from apps.common.models import BaseModel


class InstitutionalUnitQuerySet(models.QuerySet):
    def bulk_create(self, objs, *args, **kwargs):
        objs = list(objs)
        if any(obj.parent_id is not None for obj in objs):
            raise ValidationError(
                "Unidades com unidade superior devem ser salvas individualmente para validar a hierarquia."
            )
        return super().bulk_create(objs, *args, **kwargs)

    def bulk_update(self, objs, fields, *args, **kwargs):
        if {"parent", "parent_id"}.intersection(fields):
            raise ValidationError(
                "A hierarquia institucional não pode ser alterada com bulk_update()."
            )
        return super().bulk_update(objs, fields, *args, **kwargs)


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
    display_order = models.PositiveIntegerField(default=0)

    objects = InstitutionalUnitQuerySet.as_manager()

    class Meta:
        ordering = ("display_order", "name")
        verbose_name = "unidade institucional"
        verbose_name_plural = "unidades institucionais"
        constraints = [
            models.CheckConstraint(
                check=~Q(parent=F("id")),
                name="institutional_unit_parent_not_self",
            ),
        ]

    def __str__(self) -> str:
        return self.acronym or self.name

    def clean(self) -> None:
        super().clean()
        if self.parent_id is None:
            return

        ancestor_id = self.parent_id
        visited_ids = set()
        while ancestor_id is not None:
            if ancestor_id == self.pk or ancestor_id in visited_ids:
                raise ValidationError(
                    {"parent": "A unidade superior não pode criar um ciclo na hierarquia institucional."}
                )
            visited_ids.add(ancestor_id)
            ancestor_id = (
                type(self).objects.filter(pk=ancestor_id).values_list("parent_id", flat=True).first()
            )

    def save(self, *args, **kwargs):
        # QuerySet.update() is the only intentionally unsupported ORM bypass.
        self.full_clean()
        return super().save(*args, **kwargs)


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
        constraints = [
            models.UniqueConstraint(
                fields=("person", "unit", "role"),
                name="unique_institution_membership",
            ),
            models.CheckConstraint(
                check=(
                    Q(start_date__isnull=True)
                    | Q(end_date__isnull=True)
                    | Q(end_date__gte=F("start_date"))
                ),
                name="valid_membership_date_range",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.person} — {self.role} em {self.unit}"

    def clean(self) -> None:
        super().clean()
        if self.start_date and self.end_date and self.end_date < self.start_date:
            raise ValidationError(
                {"end_date": "A data de término deve ser igual ou posterior à data de início."}
            )

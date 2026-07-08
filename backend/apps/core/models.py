from django.db import models

from apps.common.models import BaseModel


class SiteSettings(BaseModel):
    site_name = models.CharField(max_length=120, default="LATEC.IN")
    description = models.TextField(blank=True)
    institution = models.CharField(max_length=180, blank=True)
    contact_email = models.EmailField(blank=True)
    logo = models.ImageField(upload_to="core/logos/", blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "configuração do site"
        verbose_name_plural = "configurações do site"

    def __str__(self) -> str:
        return self.site_name


class HeroBanner(BaseModel):
    title = models.CharField(max_length=180)
    subtitle = models.TextField(blank=True)
    cta_label = models.CharField(max_length=80, blank=True)
    cta_url = models.CharField(max_length=240, blank=True)
    image = models.ImageField(upload_to="core/heroes/", blank=True)
    is_published = models.BooleanField(default=False)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("display_order", "title")
        verbose_name = "banner principal"
        verbose_name_plural = "banners principais"

    def __str__(self) -> str:
        return self.title


class InstitutionalSection(BaseModel):
    class SectionType(models.TextChoices):
        MISSION = "mission", "Missão"
        VISION = "vision", "Visão"
        VALUES = "values", "Valores"
        HISTORY = "history", "Histórico"
        PURPOSE = "purpose", "Propósito"

    section_type = models.CharField(max_length=32, choices=SectionType.choices)
    title = models.CharField(max_length=140)
    slug = models.SlugField(max_length=160, unique=True)
    content = models.TextField()
    image = models.ImageField(upload_to="core/sections/", blank=True)
    is_published = models.BooleanField(default=False)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("display_order", "title")
        verbose_name = "seção institucional"
        verbose_name_plural = "seções institucionais"

    def __str__(self) -> str:
        return self.title


class SocialLink(BaseModel):
    label = models.CharField(max_length=80)
    url = models.URLField()
    icon = models.CharField(max_length=80, blank=True)
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("display_order", "label")
        verbose_name = "link social"
        verbose_name_plural = "links sociais"

    def __str__(self) -> str:
        return self.label

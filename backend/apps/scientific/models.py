from django.db import models

from apps.common.models import BaseModel, EditorialStatus


class ScientificOutput(BaseModel):
    class OutputType(models.TextChoices):
        ARTICLE = "article", "Artigo"
        ABSTRACT = "abstract", "Resumo"
        PATENT = "patent", "Patente"
        EBOOK = "ebook", "E-book"
        BOOK = "book", "Livro"
        TECHNICAL_REPORT = "technical_report", "Relatório técnico"
        PROJECT = "project", "Projeto"
        SCIENTIFIC_PRODUCTION = "scientific_production", "Produção científica"

    title = models.CharField(max_length=220)
    slug = models.SlugField(max_length=240, unique=True)
    output_type = models.CharField(max_length=40, choices=OutputType.choices)
    axis = models.ForeignKey("axes.ResearchAxis", on_delete=models.SET_NULL, related_name="scientific_outputs", blank=True, null=True)
    authors = models.TextField(blank=True)
    abstract = models.TextField(blank=True)
    publication_date = models.DateField(blank=True, null=True)
    file = models.FileField(upload_to="scientific/", blank=True)
    external_url = models.URLField(blank=True)
    status = models.CharField(max_length=32, choices=EditorialStatus.choices, default=EditorialStatus.DRAFT)
    is_published = models.BooleanField(default=False)
    published_at = models.DateTimeField(blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("display_order", "-publication_date", "title")
        verbose_name = "produção científica"
        verbose_name_plural = "produções científicas"

    def __str__(self) -> str:
        return self.title

from django.db import models

from apps.common.models import BaseModel, EditorialStatus


class TransparencyDocument(BaseModel):
    class DocumentType(models.TextChoices):
        NOTICE = "notice", "Edital"
        MINUTES = "minutes", "Ata"
        HOMOLOGATION = "homologation", "Homologação"
        APPEAL_JUDGMENT = "appeal_judgment", "Julgamento de recurso"
        RESULT = "result", "Resultado"
        STATEMENT = "statement", "Comunicado"

    title = models.CharField(max_length=180)
    slug = models.SlugField(max_length=200, unique=True)
    document_type = models.CharField(max_length=40, choices=DocumentType.choices)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to="transparency/")
    publication_date = models.DateField(blank=True, null=True)
    related_process = models.CharField(max_length=160, blank=True)
    status = models.CharField(max_length=32, choices=EditorialStatus.choices, default=EditorialStatus.DRAFT)
    is_published = models.BooleanField(default=False)
    published_at = models.DateTimeField(blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("display_order", "-publication_date", "title")
        verbose_name = "documento de transparência"
        verbose_name_plural = "documentos de transparência"

    def __str__(self) -> str:
        return self.title

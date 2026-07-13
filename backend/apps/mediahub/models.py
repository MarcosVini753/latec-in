from django.conf import settings
from django.db import models

from apps.common.models import BaseModel


class MediaAsset(BaseModel):
    class AssetType(models.TextChoices):
        IMAGE = "image", "Imagem"
        PDF = "pdf", "PDF"
        EBOOK = "ebook", "E-book"
        BOOK = "book", "Livro"
        DOCUMENT = "document", "Documento"
        CERTIFICATE = "certificate", "Certificado"
        TECHNICAL = "technical", "Documento técnico"
        OTHER = "other", "Outro"

    title = models.CharField(max_length=180)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to="mediahub/")
    asset_type = models.CharField(max_length=32, choices=AssetType.choices, default=AssetType.DOCUMENT)
    alt_text = models.CharField(max_length=240, blank=True)
    credit = models.CharField(max_length=180, blank=True)
    is_public = models.BooleanField(default=True)
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="uploaded_media_assets",
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ("title",)
        verbose_name = "ativo de mídia"
        verbose_name_plural = "ativos de mídia"

    def __str__(self) -> str:
        return self.title

from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField("criado em", auto_now_add=True)
    updated_at = models.DateTimeField("atualizado em", auto_now=True)

    class Meta:
        abstract = True


class EditorialStatus(models.TextChoices):
    DRAFT = "draft", "Rascunho"
    IN_REVIEW = "in_review", "Em revisão"
    PUBLISHED = "published", "Publicado"
    ARCHIVED = "archived", "Arquivado"

from django.db import models

from apps.common.models import BaseModel


class Partner(BaseModel):
    class PartnerType(models.TextChoices):
        ACADEMIC = "academic", "Acadêmico"
        INSTITUTIONAL = "institutional", "Institucional"
        PRODUCTIVE_SECTOR = "productive_sector", "Setor produtivo"
        COMMUNITY = "community", "Comunidade"
        OTHER = "other", "Outro"

    name = models.CharField(max_length=160)
    slug = models.SlugField(max_length=180, unique=True)
    partner_type = models.CharField(max_length=40, choices=PartnerType.choices, default=PartnerType.INSTITUTIONAL)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to="partnerships/logos/", blank=True)
    website = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("display_order", "name")
        verbose_name = "parceiro"
        verbose_name_plural = "parceiros"

    def __str__(self) -> str:
        return self.name


class ContactMessage(BaseModel):
    class ContactType(models.TextChoices):
        QUESTIONS = "questions", "Dúvidas"
        PRESS = "press", "Imprensa"
        PARTNERSHIP = "partnership", "Quero ser parceiro"
        SELECTION_PROCESS = "selection_process", "Processo seletivo"
        OTHER = "other", "Outro"

    class MessageStatus(models.TextChoices):
        NEW = "new", "Nova"
        IN_PROGRESS = "in_progress", "Em atendimento"
        ANSWERED = "answered", "Respondida"
        ARCHIVED = "archived", "Arquivada"

    contact_type = models.CharField(max_length=32, choices=ContactType.choices, default=ContactType.OTHER)
    subject = models.CharField(max_length=160)
    name = models.CharField(max_length=140)
    email = models.EmailField()
    organization = models.CharField(max_length=160, blank=True)
    message = models.TextField()
    status = models.CharField(max_length=32, choices=MessageStatus.choices, default=MessageStatus.NEW)
    responded_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "mensagem de contato"
        verbose_name_plural = "mensagens de contato"

    def __str__(self) -> str:
        return f"{self.get_contact_type_display()} - {self.subject} - {self.name}"

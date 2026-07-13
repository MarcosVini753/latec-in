from django.conf import settings
from django.db import models

from apps.common.models import BaseModel


class Profile(BaseModel):
    class AdminRole(models.TextChoices):
        ADMIN = "admin", "Administrador"
        COORDINATOR = "coordinator", "Coordenadora"
        MENTOR = "mentor", "Mentor/Professor"
        EDITOR = "editor", "Editor"
        READER = "reader", "Leitor administrativo"

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    person = models.OneToOneField(
        "people.Person",
        on_delete=models.SET_NULL,
        related_name="admin_profile",
        blank=True,
        null=True,
    )
    role = models.CharField(max_length=32, choices=AdminRole.choices, default=AdminRole.READER)
    is_active_admin = models.BooleanField(default=True)

    class Meta:
        verbose_name = "perfil administrativo"
        verbose_name_plural = "perfis administrativos"

    def __str__(self) -> str:
        return f"{self.user} ({self.get_role_display()})"

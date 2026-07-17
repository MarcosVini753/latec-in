from django.db import models

from apps.common.models import BaseModel, EditorialStatus


class LearningTrack(BaseModel):
    unit = models.ForeignKey(
        "institutional.InstitutionalUnit",
        on_delete=models.SET_NULL,
        related_name="learning_tracks",
        blank=True,
        null=True,
    )
    title = models.CharField(max_length=160)
    slug = models.SlugField(max_length=180, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("display_order", "title")
        verbose_name = "trilha de aprendizagem"
        verbose_name_plural = "trilhas de aprendizagem"

    def __str__(self) -> str:
        return self.title


class Course(BaseModel):
    class EnrollmentStatus(models.TextChoices):
        OPEN = "open", "Inscrições abertas"
        COMING_SOON = "coming_soon", "Em breve"
        CLOSED = "closed", "Inscrições encerradas"
        COMPLETED = "completed", "Concluído"

    unit = models.ForeignKey(
        "institutional.InstitutionalUnit",
        on_delete=models.SET_NULL,
        related_name="courses",
        blank=True,
        null=True,
    )
    title = models.CharField(max_length=180)
    slug = models.SlugField(max_length=200, unique=True)
    track = models.ForeignKey(LearningTrack, on_delete=models.SET_NULL, related_name="courses", blank=True, null=True)
    axis = models.ForeignKey("axes.ResearchAxis", on_delete=models.SET_NULL, related_name="courses", blank=True, null=True)
    instructors = models.ManyToManyField("people.Person", related_name="courses", blank=True)
    description = models.TextField(blank=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    workload_hours = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    enrollment_status = models.CharField(max_length=32, choices=EnrollmentStatus.choices, default=EnrollmentStatus.COMING_SOON)
    editorial_status = models.CharField(max_length=32, choices=EditorialStatus.choices, default=EditorialStatus.DRAFT)
    registration_url = models.URLField(blank=True)
    cover_image = models.ImageField(upload_to="learning/courses/", blank=True)
    is_published = models.BooleanField(default=False)
    published_at = models.DateTimeField(blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("display_order", "-start_date", "title")
        verbose_name = "curso"
        verbose_name_plural = "cursos"

    def __str__(self) -> str:
        return self.title


class CourseMaterial(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="materials")
    title = models.CharField(max_length=160)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to="learning/materials/", blank=True)
    external_url = models.URLField(blank=True)
    is_public = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("display_order", "title")
        verbose_name = "material de curso"
        verbose_name_plural = "materiais de curso"

    def __str__(self) -> str:
        return self.title


class Event(BaseModel):
    class EventStatus(models.TextChoices):
        SCHEDULED = "scheduled", "Agendado"
        OPEN = "open", "Inscrições abertas"
        COMPLETED = "completed", "Realizado"
        CANCELED = "canceled", "Cancelado"

    unit = models.ForeignKey(
        "institutional.InstitutionalUnit",
        on_delete=models.SET_NULL,
        related_name="events",
        blank=True,
        null=True,
    )
    title = models.CharField(max_length=180)
    slug = models.SlugField(max_length=200, unique=True)
    event_type = models.CharField(max_length=80)
    axis = models.ForeignKey("axes.ResearchAxis", on_delete=models.SET_NULL, related_name="events", blank=True, null=True)
    description = models.TextField(blank=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    location = models.CharField(max_length=180, blank=True)
    registration_url = models.URLField(blank=True)
    event_status = models.CharField(max_length=32, choices=EventStatus.choices, default=EventStatus.SCHEDULED)
    editorial_status = models.CharField(max_length=32, choices=EditorialStatus.choices, default=EditorialStatus.DRAFT)
    is_published = models.BooleanField(default=False)
    published_at = models.DateTimeField(blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("display_order", "-start_date", "title")
        verbose_name = "evento"
        verbose_name_plural = "eventos"

    def __str__(self) -> str:
        return self.title

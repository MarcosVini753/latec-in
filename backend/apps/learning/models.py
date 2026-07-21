from django.db import models

from apps.common.models import BaseModel, EditorialStatus


class Course(BaseModel):
    class EnrollmentStatus(models.TextChoices):
        OPEN = "open", "Inscrições abertas"
        COMING_SOON = "coming_soon", "Em breve"
        CLOSED = "closed", "Inscrições encerradas"
        COMPLETED = "completed", "Concluído"

    unit = models.ForeignKey(
        "institutional.InstitutionalUnit",
        on_delete=models.PROTECT,
        related_name="courses",
    )
    title = models.CharField(max_length=180)
    slug = models.SlugField(max_length=200, unique=True)
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
    published_at = models.DateTimeField(blank=True, null=True)
    include_in_parent_ecosystem = models.BooleanField(
        default=False,
        help_text="Inclui este conteúdo no recorte público da unidade mãe.",
    )

    class Meta:
        ordering = ("-start_date", "title")
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
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("display_order", "title")
        verbose_name = "material de curso"
        verbose_name_plural = "materiais de curso"

    def __str__(self) -> str:
        return self.title

from django.db import models

from apps.common.models import BaseModel


class Person(BaseModel):
    full_name = models.CharField(max_length=180)
    slug = models.SlugField(max_length=200, unique=True)
    short_bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to="people/", blank=True)
    email = models.EmailField(blank=True)
    lattes_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    website_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("display_order", "full_name")
        verbose_name = "pessoa"
        verbose_name_plural = "pessoas"

    def __str__(self) -> str:
        return self.full_name

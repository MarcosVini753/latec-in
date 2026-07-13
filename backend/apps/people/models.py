from django.db import models

from apps.common.models import BaseModel


class Role(BaseModel):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("display_order", "name")
        verbose_name = "função pública"
        verbose_name_plural = "funções públicas"

    def __str__(self) -> str:
        return self.name


class Person(BaseModel):
    full_name = models.CharField(max_length=180)
    slug = models.SlugField(max_length=200, unique=True)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, related_name="people", blank=True, null=True)
    short_bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to="people/", blank=True)
    email = models.EmailField(blank=True)
    lattes_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    website_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("display_order", "full_name")
        verbose_name = "pessoa"
        verbose_name_plural = "pessoas"

    def __str__(self) -> str:
        return self.full_name

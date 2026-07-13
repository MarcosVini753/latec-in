from django.db import models

from apps.common.models import BaseModel, EditorialStatus


class PostCategory(BaseModel):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("display_order", "name")
        verbose_name = "categoria de post"
        verbose_name_plural = "categorias de post"

    def __str__(self) -> str:
        return self.name


class Tag(BaseModel):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        ordering = ("name",)
        verbose_name = "tag"
        verbose_name_plural = "tags"

    def __str__(self) -> str:
        return self.name


class Post(BaseModel):
    title = models.CharField(max_length=180)
    slug = models.SlugField(max_length=200, unique=True)
    axis = models.ForeignKey("axes.ResearchAxis", on_delete=models.SET_NULL, related_name="posts", blank=True, null=True)
    category = models.ForeignKey(PostCategory, on_delete=models.SET_NULL, related_name="posts", blank=True, null=True)
    tags = models.ManyToManyField(Tag, related_name="posts", blank=True)
    authors = models.ManyToManyField("people.Person", related_name="posts", blank=True)
    summary = models.TextField(blank=True)
    content = models.TextField()
    cover_image = models.ImageField(upload_to="news/posts/", blank=True)
    status = models.CharField(max_length=32, choices=EditorialStatus.choices, default=EditorialStatus.DRAFT)
    published_at = models.DateTimeField(blank=True, null=True)
    is_published = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("display_order", "-published_at", "title")
        verbose_name = "post"
        verbose_name_plural = "posts"

    def __str__(self) -> str:
        return self.title

from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.utils import timezone

# Create your models here.
class Status(models.Model):
    name = models.CharField(max_length=20, unique=True)
    slug = models.SlugField(max_length=20, unique=True)

class Meta:
    verbose_name_plural = "Statuses"
    ordering = ["name"]
    
    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    body = models.TextField()
    status = models.ForeignKey(Status, on_delete=models.PROTECT, related_name="posts")
    published_at = models.DateTimeField(null=True, blank=True, help_text="Set when status is 'published'.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-published_at", "-created_at"]
        indexes = [models.Index(fields=["slug"])]

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug[:220]
            counter = 1
            while Post.objects.filter(slug=slug).exists():
                slug = f"{base_slug[:216]}-{counter}"  # Reserve space for counter
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("blog:post_detail", args=[self.slug])

    def __str__(self):
        return self.title

    def is_published(self):
        return self.status.name.lower() == 'published' and self.published_at is not None
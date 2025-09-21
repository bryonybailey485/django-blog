from django.contrib import admin
from django.contrib import admin
from .models import Status, Post


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "published_at", "created_at", "is_published")
    list_filter = ("status", "created_at")
    search_fields = ("title", "body")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "published_at"
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'body')
        }),
        ('Status', {
            'fields': ('status', 'published_at')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        # Automatically set published_at if status is published
        if obj.status.name.lower() == 'published' and not obj.published_at:
            obj.published_at = timezone.now()
        super().save_model(request, obj, form, change)
# Register your models here.

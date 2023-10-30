from django.contrib import admin
from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "user",
        "category",
        "is_approved",
    )

    search_fields = (
        "title",
        "=user__username",
    )

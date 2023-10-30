from django.contrib import admin
from .models import Project


@admin.register(Project)
class PhotoAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "user",
    )

    search_fields = (
        "title",
        "=user__username",
    )

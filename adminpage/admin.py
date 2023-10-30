from django.contrib import admin
from .models import Approval


@admin.register(Approval)
class ApprovalAdmin(admin.ModelAdmin):
    list_display = ("kind",)
    list_filter = ("kind",)

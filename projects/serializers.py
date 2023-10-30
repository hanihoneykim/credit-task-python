from rest_framework import serializers
from .models import Project


class ProjectEditorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"

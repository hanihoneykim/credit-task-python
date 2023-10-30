from rest_framework import serializers
from .models import Project
from users.serializers import TinyUserSerializer
from categories.serializers import TinyCategorySerializer


class ProjectEditorSerializer(serializers.ModelSerializer):
    user = TinyUserSerializer(read_only=True)
    category = TinyCategorySerializer(read_only=True)
    is_approved = serializers.CharField(source="get_is_approved_display")

    class Meta:
        model = Project
        fields = (
            "title",
            "photo",
            "description",
            "user",
            "category",
            "is_approved",
        )

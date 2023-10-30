from rest_framework import serializers
from .models import Project
from users.serializers import TinyUserSerializer
from categories.serializers import TinyCategorySerializer


class ProjectEditorSerializer(serializers.ModelSerializer):
    user = TinyUserSerializer(read_only=True)
    category = TinyCategorySerializer(read_only=True)

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


class TinyProjectSerializer(serializers.ModelSerializer):
    user = TinyUserSerializer(read_only=True)
    category = TinyCategorySerializer(read_only=True)

    class Meta:
        model = Project
        fields = (
            "pk",
            "title",
            "user",
            "category",
            "is_approved",
        )


class PublicProjectSerializer(serializers.ModelSerializer):
    user = TinyUserSerializer(read_only=True)
    category = TinyCategorySerializer(read_only=True)

    class Meta:
        model = Project
        fields = (
            "pk",
            "title",
            "photo",
            "description",
            "user",
            "category",
        )

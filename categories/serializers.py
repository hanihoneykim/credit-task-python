from rest_framework import serializers
from .models import Category


class TinyCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "pk",
            "name",
            "kind",
        )

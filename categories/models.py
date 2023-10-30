from django.db import models


class Category(models.Model):
    """Model Definition for Categories"""

    class CategoryKindChoices(models.TextChoices):
        STATIONERY = "stationery", "문구류"
        DIGITAL = "digital", "디지털"
        CHARACTER = "character", "캐릭터"
        LIVING = "living", "리빙"
        PET = "pet", "반려동물"

    name = models.CharField(max_length=50)
    kind = models.CharField(
        max_length=15,
        choices=CategoryKindChoices.choices,
    )

    def __str__(self) -> str:
        return f"{self.kind.title()}: {self.name}"

    class Meta:
        verbose_name_plural = "Categories"

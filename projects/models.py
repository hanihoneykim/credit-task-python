from django.db import models
from common.models import CommonModel


class Project(CommonModel):

    """Model Definition for Project"""

    class ApprovalKindChoices(models.TextChoices):
        APPROVAL = "approval", "승인"
        DISAPPROVAL = "disapproval", "미승인"
        UNDER_REVIEW = "under_review", "검토중"

    title = models.CharField(
        max_length=200,
        default="",
        verbose_name="제목",
    )
    photo = models.URLField(
        null=True,
        default="",
        verbose_name="사진파일",
    )
    description = models.TextField(
        blank=True,
        verbose_name="내용",
    )
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        verbose_name="작성자",
        related_name="projects",
    )
    category = models.ForeignKey(
        "categories.Category",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="projects",
    )
    is_approved = models.CharField(
        max_length=15,
        choices=ApprovalKindChoices.choices,
        default=ApprovalKindChoices.UNDER_REVIEW,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

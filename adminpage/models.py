from django.db import models


class Approval(models.Model):
    """승인/미승인/검토중 model"""

    class ApprovalKindChoices(models.TextChoices):
        APPROVAL = "approval", "승인"
        DISAPPROVAL = "disapproval", "미승인"
        UNDER_REVIEW = "under_review", "검토중"

    kind = models.CharField(
        max_length=15,
        choices=ApprovalKindChoices.choices,
    )

    def __str__(self) -> str:
        return self.kind

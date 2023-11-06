import uuid

from django.db import models


class UUIDModel(models.Model):
    """
    An abstract base model with a UUID as its primary key.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class TimestampedModel(models.Model):
    """
    An abstract base model that provides creation and update timestamps.
    """

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

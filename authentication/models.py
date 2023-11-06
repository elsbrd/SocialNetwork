from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from common.models import TimestampedModel, UUIDModel


class User(AbstractUser, UUIDModel, TimestampedModel):
    email = models.EmailField(unique=True)

    last_request = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Stores the timestamp of the last request made by a user.",
    )

    def reset_last_login_time(self):
        self.last_login = timezone.now()
        self.save(update_fields=['last_login'])

    def reset_last_request_time(self):
        self.last_request = timezone.now()
        self.save(update_fields=['last_request'])
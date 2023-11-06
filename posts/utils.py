import datetime
from typing import Optional

from django.conf import settings
from rest_framework.exceptions import ValidationError


def parse_date(dt: Optional[str], fmt: str = '%Y-%m-%d'):
    if dt:
        try:
            return datetime.datetime.strptime(dt, fmt).date()
        except ValueError:
            raise ValidationError({settings.NON_FIELD_ERRORS_KEY: ['Invalid date format. Use YYYY-MM-DD.']})

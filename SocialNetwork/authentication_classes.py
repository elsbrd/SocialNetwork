from typing import Optional

from rest_framework.request import Request
from rest_framework_simplejwt.authentication import JWTAuthentication


class MyJWTAuthentication(JWTAuthentication):
    def authenticate(self, request: Request) -> Optional[tuple]:
        result = super().authenticate(request)

        if result is not None:
            user, token = result  # If authentication succeeds, result is a tuple of (user, token)
            user.reset_last_request_time()

        return result
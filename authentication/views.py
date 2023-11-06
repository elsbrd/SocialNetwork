from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, views
from rest_framework.request import Request

from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from authentication.serializers import SignupSerializer, UserActivitySerializer, MyTokenObtainPairSerializer
from rest_framework.exceptions import ValidationError as DRFValidationError
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework_simplejwt.views import TokenObtainPairView
from django.utils import timezone
User = get_user_model()


class SignupView(generics.CreateAPIView):
    """
    API endpoint for user registration.
    Allows any unauthenticated user to sign up.
    """

    authentication_classes = ()
    permission_classes = (permissions.AllowAny,)

    queryset = User.objects.all()
    serializer_class = SignupSerializer


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    user: User # is set in serializer

    def post(self, request: Request, *args, **kwargs) -> Response:
        response = super().post(request, *args, **kwargs)

        # If we successfully fulfill the login request (i.e., status code 200 OK),
        # update the last login time for the user.
        if response.status_code == HTTP_200_OK:
            self.user.reset_last_login_time()

        return response


class UserActivityView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserActivitySerializer

    def get_object(self):
        if user_id := self.request.query_params.get("user"):
            try:
                user = get_object_or_404(User, id=user_id)

            except DjangoValidationError as e:
                raise DRFValidationError({"detail": e.messages})

        else:
            user = self.request.user

        return user




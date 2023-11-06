from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views

app_name = "authentication"

urlpatterns = [
    path("signup/", views.SignupView.as_view(), name="signup"),
    path('token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user-activity/', views.UserActivityView.as_view(), name='user-activity')
]
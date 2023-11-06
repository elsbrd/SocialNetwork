from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

app_name = "posts_app"


router = DefaultRouter()

router.register("posts", views.PostViewSet, basename="posts")

urlpatterns = [
    path("likes/analytics/", views.LikeAnalyticsView.as_view(), name="likes-analytics")
]

urlpatterns += router.urls

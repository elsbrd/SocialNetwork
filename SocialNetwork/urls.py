from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api/",
        include(
            [
                path("authentication/", include("authentication.urls")),
                path("", include("posts.urls")),
            ]
        ),
    ),
]

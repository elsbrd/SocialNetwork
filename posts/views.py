from django.db import IntegrityError
from django.db.models import Count, Q
from django.db.models.functions import TruncDate

from rest_framework import mixins, viewsets, views
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import (
    ValidationError as DRFValidationError,
    PermissionDenied,
)
from django.core.exceptions import ValidationError as DjangoValidationError
from posts.models import Post, Like
from posts.serializers import PostSerializer


class PostViewSet(
    mixins.CreateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.validated_data["user"] = self.request.user
        serializer.save()

    @action(detail=True, methods=["post"])
    def like(self, request, *args, **kwargs):
        try:
            Like.objects.create(post=self.get_object(), user=self.request.user)
        except IntegrityError:
            # Skip this error because user can like post only once
            pass

        return Response()

    @action(detail=True, methods=["post"])
    def unlike(self, request, *args, **kwargs):
        Like.objects.filter(post=self.get_object(), user=self.request.user).delete()
        return Response()


class LikeAnalyticsView(views.APIView):
    def get(self, request, *args, **kwargs):
        period_filter = self._parse_period_query_params()
        user_filter = self._parse_user_query_params()

        filters = period_filter & user_filter

        try:
            likes_per_day = (
                Like.objects.filter(filters)
                .annotate(date=TruncDate("created_at"))
                .values("date")
                .annotate(likes_count=Count("id"))
                .order_by("date")
            )

        except DjangoValidationError as e:
            raise DRFValidationError({"detail": e.messages})

        return Response(likes_per_day)

    def _parse_period_query_params(self):
        q = Q()

        if date_from := self.request.query_params.get("date_from"):
            q &= Q(created_at__date__gte=date_from)

        if date_to := self.request.query_params.get("date_to"):
            q &= Q(created_at__date__lte=date_to)

        return q

    def _parse_user_query_params(self):
        default_query = Q(post__user__id=self.request.user.id)

        user_id = self.request.query_params.get("user")
        if not user_id:
            return default_query  # Return early if no user query param

        if not self.request.user.is_superuser:
            raise PermissionDenied(
                {
                    "detail": f'Only superusers are allowed to request '
                              f'{"all users" if user_id == "all" else "other users"} '
                              f'analytics.'
                }
            )

        if user_id == "all":
            return Q()

        elif user_id != self.request.user.id:
            return Q(post__user__id=user_id)

        return default_query

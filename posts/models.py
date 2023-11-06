from django.contrib.auth import get_user_model
from django.db import models, transaction

from common.models import UUIDModel, TimestampedModel

User = get_user_model()


class Post(UUIDModel, TimestampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=100)
    content = models.TextField()

    likes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'Post("{self.title}" by {self.user})'


class Like(UUIDModel, TimestampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'post'], name='unique_like')
        ]

    def __str__(self):
        return f'Like({self.user} liked {self.post})'
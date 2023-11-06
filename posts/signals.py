from django.db.models import F
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from posts.models import Like


@receiver(post_save, sender=Like)
def handle_post_like(sender, instance, created, **kwargs):
    if created:
        # use F() expression to avoid race-condition
        instance.post.likes = F('likes') + 1
        instance.post.save()


@receiver(post_delete, sender=Like)
def handle_post_unlike(sender, instance, **kwargs):
    instance.post.likes = F('likes') - 1
    instance.post.save()
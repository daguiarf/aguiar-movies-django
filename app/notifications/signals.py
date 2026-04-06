from django.db.models.signals import post_save
from django.dispatch import receiver

from forum.models import PostLike, Comment


@receiver(post_save, sender=PostLike)
def on_post_like(sender, instance, created, **kwargs):
    if not created:
        return
    from .tasks import create_like_notification
    create_like_notification.delay(instance.pk)


@receiver(post_save, sender=Comment)
def on_comment_created(sender, instance, created, **kwargs):
    if not created:
        return
    from .tasks import create_comment_notification
    create_comment_notification.delay(instance.pk)

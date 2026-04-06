from celery import shared_task


@shared_task
def create_like_notification(like_id: int):
    from forum.models import PostLike
    from .models import Notification

    try:
        like = PostLike.objects.select_related("user", "post__user").get(pk=like_id)
    except PostLike.DoesNotExist:
        return

    if like.user == like.post.user:
        return

    Notification.objects.get_or_create(
        recipient=like.post.user,
        sender=like.user,
        notification_type=Notification.LIKE,
        post=like.post,
    )


@shared_task
def create_comment_notification(comment_id: int):
    from forum.models import Comment
    from .models import Notification

    try:
        comment = Comment.objects.select_related("user", "post__user").get(pk=comment_id)
    except Comment.DoesNotExist:
        return

    if comment.user == comment.post.user:
        return

    Notification.objects.create(
        recipient=comment.post.user,
        sender=comment.user,
        notification_type=Notification.COMMENT,
        post=comment.post,
    )

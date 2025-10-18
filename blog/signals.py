from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import Notification

from .models import Comment, Post


@receiver(post_save, sender=Post)
def post_activity(sender, instance, created, **kwargs):
    # وقتی پست ساخته شد یا به‌روزرسانی شد، notification برای نویسنده ثبت کن
    title = "Post created" if created else "Post updated"
    Notification.objects.create(
        user=instance.author,
        title=title,
        message=f"Your post '{instance.title}' was {'created' if created else 'updated'}.",
        notif_type="post",
    )


@receiver(post_save, sender=Comment)
def comment_activity(sender, instance, created, **kwargs):
    if created:
        # اطلاع به نویسنده پست که کامنت جدیدی وجود دارد
        Notification.objects.create(
            user=instance.post.author,
            title="New comment",
            message=f"{instance.author.username} commented on your post '{instance.post.title}'.",
            notif_type="comment",
        )

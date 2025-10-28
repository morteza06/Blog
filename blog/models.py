from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone

from .utils import unique_slugify


class Tag(models.Model):
    name = models.CharField(unique=True, max_length=50)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Post(models.Model):
    STATUS_CHOICES = [
        ("draft", "پیش نویس"),
        ("published", "منتشرشده"),
        ("archived", "آرشیو"),
    ]
    # استفاده از settings.AUTH_USER_MODEL به جای auth.User
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posts"
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(blank=True, null=True)
    is_published = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="draft")
    tags = models.ManyToManyField(Tag, related_name="posts", blank=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            unique_slugify(self, self.title)
        # اگر is_published تنظیم شده ولی published_at خالی است، اکنون را ست کن
        if self.is_published and not self.published_at:
            self.published_at = timezone.now()
            # هنگام save() اگر slug خالی بود از عنوان slug می‌سازد و در صورت تکرار، عدد الحاق می‌کند تا یکتا شود.
        super().save(*args, **kwargs)

    def publish(self):
        """تغییر وضعیت پست به منتشر شده"""
        self.status = "published"
        self.is_published = True
        self.published_at = timezone.now()
        self.save()

    def get_absolute_url(self):
        return reverse("blog:post_detail", args=[self.slug])

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments"
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=True)

    def __str__(self):
        return f"Comment by {self.author} on {self.post}"

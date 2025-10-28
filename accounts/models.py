from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from PIL import Image


def validate_avatar(image):
    """
    هدف : اعتبارسنجی داده در سطح پایگاه داده و هر ورودی مستقیم به مدل.
        پیام خطا برای کاربر:معمولاً پیام خام یا ValidationError
    """
    max_size = 2 * 1024 * 1024  # 2MB
    valid_extensions = ["jpg", "jpeg", "png"]

    # نوع فایل
    ext = image.name.split(".")[-1].lower()
    if ext not in valid_extensions:
        raise ValidationError("فرمت فایل باید jpg یا png باشد.")

    # حجم فایل
    if image.size > max_size:
        raise ValidationError("حجم تصویر نباید بیش از ۲ مگابایت باشد.")

    # ابعاد تصویر
    img = Image.open(image)
    width, height = img.size
    if width > 2000 or height > 2000:
        raise ValidationError(
            "ابعاد تصویر بیش از حد بزرگ است (حداکثر 2000x2000 پیکسل)."
        )


class CustomUser(AbstractUser):
    """OR Profile Model----گسترش User با اطلاعات اضافی"""

    display_name = models.CharField(max_length=100, blank=True)
    avatar = models.ImageField(
        upload_to="images/avatars/",
        validators=[validate_avatar],
        blank=True,
        null=True,
        help_text="تصویر پروفایل شما (حداکثر 2MB و ابعاد 2000x2000)",
    )
    birth_date = models.DateField(blank=True, null=True)
    profile_note = models.TextField(blank=True, help_text="پیام یا توضیح وضعیت")
    is_verified = models.BooleanField(default=False)
    joined_at = models.DateTimeField(auto_now_add=True)

    # اضافه کردن related_name برای جلوگیری از تداخل با auth.User
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="customuser_set",
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="customuser_set",
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )

    def __str__(self):
        return self.username or self.email


# مدل نمونه برای پروژه: پست‌ها
class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="accounts_posts",  # نام unique
    )
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Notification(models.Model):
    NOTIF_TYPE_CHOICES = [
        ("info", "اطلاعات"),
        ("success", "موفقیت"),
        ("warning", "هشدار"),
        ("error", "خطا"),
        ("comment", "کامنت"),
        ("post", "پست"),
    ]
    ICON_TYPE_CHOICES = [
        ("bi-bell", "زنگوله"),
        ("bi-chat", "گفتگو"),
        ("bi-heart", "قلب"),
        ("bi-check-circle", "تایید "),
        ("bi-exclamation-circle", "هشدار"),
    ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications"
    )
    title = models.CharField(max_length=200)
    message = models.TextField(blank=True)
    notif_type = models.CharField(
        choices=NOTIF_TYPE_CHOICES, max_length=20, default="info"
    )
    icon = models.CharField(choices=ICON_TYPE_CHOICES, max_length=30, default="bi-bell")
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} → {self.user}"

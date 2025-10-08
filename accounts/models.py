from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """گسترش User با اطلاعات اضافی"""
    bio = models.TextField(blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)


# مدل نمونه برای پروژه: پست‌ها
class Post(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

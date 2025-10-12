from django.core.management.base import BaseCommand

from accounts.models import CustomUser
from blog.models import Post, Tag


class Command(BaseCommand):
    help = "Insert demo data for development and testing"

    def handle(self, *args, **options):
        u = CustomUser.objects.create_user(username="admin1", password="1234")
        Tag.objects.create(name="Django")
        Tag.objects.create(name="Python")
        Post.objects.create(
            author=u,
            title="Welcome to My Blog",
            content="اولین پست آزمایشی!",
            is_published=True,
        )
        Post.objects.create(
            author=u,
            title="Django CMS",
            content="پروژه CMS جنگو با قابلیت توسعه به REST API.",
            is_published=True,
        )
        self.stdout.write(self.style.SUCCESS("✅ Sample posts added successfully."))

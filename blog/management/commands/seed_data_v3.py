import random

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from blog.models import Comment, Post, Tag

User = get_user_model()


class Command(BaseCommand):
    help = "Create seed data for the blog app (users, posts, tags, comments)."

    def handle(self, *args, **options):
        # ایجاد کاربران نمونه
        if not User.objects.filter(username="admin1").exists():
            User.objects.create_superuser(
                username="admin1", password="admin123", email="admin@example.com"
            )
            self.stdout.write(self.style.SUCCESS("Superuser 'admin1' created."))

        users = []
        for i in range(1, 6):
            user, created = User.objects.get_or_create(
                username=f"user{i}",
                defaults={
                    "email": f"user{i}@example.com",
                    "display_name": f"User {i}",
                    "is_active": True,
                    "password": "user12345",
                },
            )
            user.set_password("user12345")
            user.save()
            users.append(user)
        self.stdout.write(self.style.SUCCESS("✅ Created 5 users."))

        # ایجاد تگ‌ها
        tag_names = ["Python", "Django", "AI", "Tech", "Life", "News"]
        tags = []
        for name in tag_names:
            tag, _ = Tag.objects.get_or_create(name=name)
            tags.append(tag)
        self.stdout.write(self.style.SUCCESS("✅ Created tags."))

        # ایجاد پست‌ها
        for i in range(1, 16):
            author = random.choice(users)
            post, created = Post.objects.get_or_create(
                title=f"Sample Post {i}",
                slug=f"sample-post-{i}",
                defaults={
                    "author": author,
                    "content": f"This is the sample content of post number {i}. " * 3,
                    "created_at": timezone.now(),
                    "published_at": timezone.now(),
                    "status": "published",
                },
            )
            post.tags.set(random.sample(tags, k=random.randint(1, 3)))
        self.stdout.write(self.style.SUCCESS("✅ Created 15 sample posts."))

        # ایجاد کامنت‌ها
        all_posts = Post.objects.all()
        for post in all_posts:
            for _ in range(random.randint(1, 4)):
                Comment.objects.create(
                    post=post,
                    user=random.choice(users),
                    content="This is a sample comment on " + post.title,
                    created_at=timezone.now(),
                )
        self.stdout.write(self.style.SUCCESS("✅ Added comments to posts."))

        self.stdout.write(self.style.SUCCESS("🎉 Database successfully seeded!"))

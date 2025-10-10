from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from blog.models import Post


class Command(BaseCommand):
    help = "Insert demo data for development and testing"

    def handle(self, *args, **options):
        User = get_user_model()

        # اگر کاربر تستی وجود ندارد، بساز
        if not User.objects.filter(username="demo").exists():
            user = User.objects.create_user(
                username="demo",
                email="demo@example.com",
                password="1234",
                display_name="Demo User",
                profile_note="این یک حساب نمایشی است برای تست داشبورد.",
                is_verified=True,
            )
            self.stdout.write(self.style.SUCCESS("✅ Demo user created."))
        else:
            user = User.objects.get(username="demo")
            self.stdout.write(self.style.WARNING("ℹ️ Demo user already exists."))

        # چند پست نمونه
        titles = [
            "نخستین پست من در وبلاگ",
            "تجربه یادگیری جنگو در پروژه واقعی",
            "چطور از تست خودکار در توسعه استفاده کنیم",
            "ترفندهایی برای مدیریت گیت در پروژه‌های تیمی",
        ]

        contents = [
            "<p>این نخستین پست من در وبلاگ است. هدف این پست آموزش مقدماتی و معرفی داشبورد کاربر است.</p>",
            "<p>تجربه یادگیری جنگو در پروژه واقعی: نکات کلیدی برای توسعه پروژه‌های چند اپی.</p>",
            "<p>چطور از تست خودکار در توسعه استفاده کنیم: pytest و coverage ابزارهای مهم هستند.</p>",
            "<p>ترفندهایی برای مدیریت گیت در پروژه‌های تیمی: Branch workflow و Commit message استاندارد.</p>",
        ]
        for i, t in enumerate(titles):
            Post.objects.get_or_create(
                author=user,
                title=t,
                defaults={"content": contents[i]},
            )

        self.stdout.write(self.style.SUCCESS("✅ Sample posts added successfully."))
        self.stdout.write(self.style.SUCCESS("✅ Sample details of posts added successfully."))
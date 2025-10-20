from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import ProfileEditForm, SignUpForm


@login_required
def dashboard(request):
    """
    کاربر وارد شده را به داشبورد خودش هدایت می‌کند
    """
    user = request.user
    # آخرین پست‌های نویسنده (۵ تا)
    recent_posts = user.posts.all().order_by("-created_at")[:5]
    # تعداد کل پست‌ها
    total_posts = user.posts.filter(author=user).count()

    # نوتیفیکیشن‌های کاربر (خوانده نشده قبل از همه)
    notifications = user.notifications.all()[:8]  # تعداد قابل تنظیم
    # فعالیت‌های اخیر ترکیبی: هم پست و هم نوتیفیکیشن (می‌توان merge کرد)
    # برای ساده‌سازی، یک لیست مرتب بر اساس created_at می‌سازیم:
    activities = []
    for p in recent_posts:
        activities.append(
            {
                "type": "post",
                "title": p.title,
                "created_at": p.created_at,
                "url": p.get_absolute_url(),
            }
        )
    for n in notifications:
        activities.append(
            {
                "type": "notif",
                "title": n.title,
                "created_at": n.created_at,
                "message": n.message,
            }
        )

    now = timezone.now()
    # تعیین پیام خوش‌آمدگویی بر اساس ساعت روز
    hour = now.hour
    if hour < 12:
        greeting = "صبح بخیر"
    elif 12 <= hour < 18:
        greeting = "عصر بخیر"
    else:
        greeting = "شب بخیر"

    # اعلان‌ها — بعداً از مدل Notification خوانده می‌شود
    notifications = [
        {"message": "پیام جدید از مدیر", "time": "۱ دقیقه پیش"},
        {"message": "پست شما تأیید شد", "time": "۱۰ دقیقه پیش"},
    ]

    # استفاده از فرم با modal form
    form = ProfileEditForm(instance=user)

    if request.method == "POST":
        form = ProfileEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "پروفایل با موفقیت ویرایش شد ✅")
            return redirect("dashboard")  # مهم برای نمایش پیام
        else:
            messages.error(request, "خطا در ویرایش اطلاعات ❌")

    context = {
        "greeting": greeting,
        "recent_posts": recent_posts,
        "total_posts": total_posts,
        "notifications": notifications,
        "activities": activities,
        "form": form,
    }
    return render(request, "accounts/dashboard.html", context)


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()  # از UserCreationForm استفاده می‌کند
            login(request, user)  # بعد از ثبت‌نام، کاربر وارد می‌شود
            return redirect("/")  # یا هر صفحه دیگری
    else:
        form = SignUpForm()
    return render(request, "accounts/signup.html", {"form": form})


User = get_user_model()


@login_required
def profile_view(request, username):
    """
    نمایش پروفایل کاربر جاری یا هر کاربر دیگر
    """
    # User = request.user
    user = get_object_or_404(User, username=username)
    posts = (
        user.posts.all().order_by("-created_at")[:10] if hasattr(user, "posts") else []
    )
    return render(
        request, "accounts/profile.html", {"profile_user": user, "posts": posts}
    )


@login_required
def notifications_list(request):
    notifications = request.user.notifications.all()
    return render(
        request, "accounts/notifications.html", {"notifications": notifications}
    )


@login_required
def notification_mark_read(request, pk):
    n = get_object_or_404(request.user.notifications, pk=pk)
    n.read = True
    n.save()
    return redirect("notifications")

import json

from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from blog.models import Comment, Post

from .forms import ProfileEditForm, SignUpForm


@login_required
def dashboard(request):
    """
    کاربر وارد شده را به داشبورد خودش هدایت می‌کند
    """

    user = request.user
    # استفاده از فرم با modal form
    # form = ProfileEditForm(request.POST or None, request.FILES or None, instance=user)
    greeting = _get_greeting()
    postsqs = Post.objects.filter(author=user)
    total_posts = postsqs.count()
    last_post = postsqs.order_by("-created_at").first()
    # تعداد کل پست‌ها
    total_posts = user.posts.filter(author=user).count()
    # آخرین پست‌های نویسنده (۵ تا)
    recent_posts = user.posts.all().order_by("-created_at")[:5]
    recent_comments = Comment.objects.filter(author=user).order_by("-created_at")[:5]
    # ساخت داده برای گراف
    post_stats_qs = (
        postsqs.annotate(month=TruncMonth("created_at"))
        .values("month")
        .annotate(count=Count("id"))
        .order_by("month")
    )

    post_stats = json.dumps(
        [
            {"month": ps["month"].strftime("%Y-%m"), "count": ps["count"]}
            for ps in post_stats_qs
        ]
    )

    # نوتیفیکیشن‌های کاربر (خوانده نشده قبل از همه)
    notifications = (
        user.notifications.all()[:8] if hasattr(user, "notifications") else []
    )
    # تعداد قابل تنظیم
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

    # اعلان‌ها — بعداً از مدل Notification خوانده می‌شود
    notifications = [
        {"message": "پیام جدید از مدیر", "time": "۱ دقیقه پیش"},
        {"message": "پست شما تأیید شد", "time": "۱۰ دقیقه پیش"},
    ]

    context = {
        "greeting": greeting,
        "user": user,
        "avatar": getattr(user, "avatar", None),
        "display_name": getattr(user, "display_name", None),
        "is_verified": getattr(user, "is_verified", False),
        "profile_note": getattr(user, "profile_note", ""),
        "total_posts": total_posts,
        "last_post": last_post,
        "recent_posts": recent_posts,
        "recent_comments": recent_comments,
        "notifications": notifications,
        "activities": activities,
        "post_stats": post_stats,  # ← این مقدار به قالب می‌رود
    }
    return render(request, "accounts/dashboard.html", context)


def _get_greeting():
    now = timezone.now()
    # تعیین پیام خوش‌آمدگویی بر اساس ساعت روز
    hour = now.hour
    if hour < 12:
        return "صبح بخیر"
    if 12 <= hour < 18:
        return "عصر بخیر"
    return "شب بخیر"


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
def profile_edit(request):
    user = request.user
    if request.method == "POST":
        if "cancel" in request.POST:
            messages.info(request, "تغییری اعمال نشد.")
            return redirect("dashboard")  # ← بازگشت به داشبورد در حالت انصراف
        form = ProfileEditForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "پروفایل با موفقیت ویرایش شد ✅")
            return redirect("dashboard")  # مهم برای نمایش پیام
        else:
            # فرم خطا دارد، HTML فرم را دوباره برمی‌گردانیم
            messages.error(request, "خطا خطایی در فرم وجود دارد. لطفاً بررسی کنید. ❌")
    else:
        form = ProfileEditForm(instance=user)

    return render(request, "accounts/profile_edit.html", {"form": form})


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

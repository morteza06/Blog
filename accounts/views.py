from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProfileEditForm, SignUpForm


@login_required
def dashboard(request):
    """
    کاربر وارد شده را به داشبورد خودش هدایت می‌کند
    """
    user = request.user
    # آخرین پست‌های نویسنده (۵ تا)
    recent_posts = user.posts.all().order_by("-created_at")[:5]
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
    context = {
        "recent_posts": recent_posts,
        "notifications": notifications,
        "activities": activities,
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


@login_required
def profile_edit(request):
    """
    صفحه ویرایش پروفایل کاربر جاری
    """
    user = request.user
    if request.method == "POST":
        form = ProfileEditForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("dashboard")
        else:
            print("Form errors:", form.errors)
    else:
        form = ProfileEditForm(instance=user)
    context = {
        "form": form,
        "section": "profile_edit",
    }
    return render(request, "accounts/profile_edit.html", context)


def profile_view(request, username):
    user = get_object_or_404(request.user, username=username)
    posts = user.posts.all().order_by("-created_at")[:10]
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
    n = get_object_or_404(request.user.notifictaion, pk=pk)
    n.read = True
    n.save()
    return redirect("notifications")

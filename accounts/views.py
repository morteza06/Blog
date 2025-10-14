from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import ProfileEditForm, SignUpForm


@login_required
def dashboard(request):
    """
    کاربر وارد شده را به داشبورد خودش هدایت می‌کند
    """
    user = request.user
    posts = user.posts.all()  # دسترسی به پست‌ها
    # TODO: اضافه کردن بخش نمایش فعالیت‌های اخیر کاربر (مثلاً پست‌های اخیر یا پیام‌ها)
    return render(request, "accounts/dashboard.html", {"user": user, "posts": posts})


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
    user = request.user
    if request.method == "POST":
        form = ProfileEditForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("dashboard")
    else:
        form = ProfileEditForm(instance=user)
    return render(request, "accounts/profile_edit.html", {"form": form})

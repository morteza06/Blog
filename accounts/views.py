from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm


@login_required
def dashboard(request):
    posts = request.user.posts.all()
    return render(request, 'accounts/dashboard.html', {'posts': posts})


def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()         # از UserCreationForm استفاده می‌کند
            login(request, user)       # بعد از ثبت‌نام، کاربر وارد می‌شود
            return redirect("/")       # یا هر صفحه دیگری
    else:
        form = SignUpForm()
    return render(request, "accounts/signup.html", {"form": form})

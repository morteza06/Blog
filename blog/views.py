from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from accounts.models import Notification

from .forms import CommentForm, PostForm
from .models import Comment, Post, Tag


# لیست پست‌ها (optimized)
def post_list(request):
    """نمایش تمام پست‌ها"""
    posts = (
        Post.objects.select_related("author")
        .prefetch_related("tags")
        .filter(is_published=True)
        .order_by("-published_at")
    )
    paginator = Paginator(posts, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "blog/post_list.html", {"page_obj": page_obj})


# نمایش پست و مدیریت کامنت (create)
def post_detail(request, slug):
    post = get_object_or_404(
        Post.objects.select_related("author").prefetch_related(
            Prefetch(
                "comments",
                queryset=Comment.objects.filter(approved=True).select_related("author"),
            )
        ),
        slug=slug,
    )
    comments = post.comments.all().order_by("-created_at")  # type: ignore
    form = CommentForm()

    # اگر می‌خواهی ثبت کامنت فقط برای کاربر لاگین شده باشد:
    if request.method == "POST" and "comment_submit" in request.POST:
        # comment_submit is button name
        if not request.user.is_authenticated:
            messages.error(request, "برای ثبت نظر باید وارد شوید.")
            return redirect(f"{reverse('login')}?next={request.path}")
        form = CommentForm(request.POST or None)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            # اگر approve باید توسط admin تایید شود، بسته به منطق شما:
            comment.approved = True
            comment.save()
            # ایجاد اعلان برای نویسنده پست
            Notification.objects.create(
                user=post.author,  # برای نویسنده پست اعلان
                title=f"نظر جدید روی پست شما: '{post.title}",
                message=f"{request.user.display_name or request.user.username} نظری ثبت کرد: {comment.content[:120]}",
                notif_type="comment",
            )
            messages.success(request, "نظر شما ثبت شد.")
            return redirect("blog:post_detail", slug=post.slug)
        else:
            # نمایش خطاها در همان صفحه
            messages.error(request, "لطفاً خطاها را اصلاح کنید.")
            #   برای نمایش فرم و کامنت ها

    return render(
        request,
        "blog/post_detail.html",
        {"post": post, "comments": comments, "form": form},
    )


# افزودن پست جدید
@login_required
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            # تنظیم تاریخ/slug و ... بر اساس مدل شما
            post.save()
            form.save_m2m()
            messages.success(request, "پست جدید ایجاد شد.")
            return redirect("blog:post_detail", slug=post.slug)
        else:
            messages.error(request, "لطفاً خطاها را اصلاح کنید.")
    else:
        form = PostForm()
    return render(request, "blog/post_form.html", {"form": form, "mode": "create"})


# ویرایش پست
@login_required
def post_edit(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if not (request.user == post.author or request.user.is_staff):
        messages.error(request, "دسترسی ندارید.")
        return redirect("blog:post_detail", slug=slug)

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "پست به‌روزرسانی شد.")
            return redirect("blog:post_detail", slug=post.slug)
        else:
            messages.error(request, "لطفاً خطاها را اصلاح کنید.")
    else:
        form = PostForm(instance=post)
    return render(
        request, "blog/post_form.html", {"form": form, "mode": "edit", "post": post}
    )


# حذف پست — تایید و سپس حذف
@login_required
def post_delete(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if not (request.user == post.author or request.user.is_staff):
        messages.error(request, "دسترسی ندارید.")
        return redirect("blog:post_detail", slug=slug)

    if request.method == "POST":
        post.delete()
        messages.success(request, "پست حذف شد.")
        return redirect("blog:home")  # یا لیست پست‌ها
    return render(request, "blog/post_confirm_delete.html", {"post": post})


def post_comment(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()

            # ایجاد اعلان برای نویسنده پست
            Notification.objects.create(
                user=post.author,
                title="نظر جدید",
                message=f"کاربر {request.user.username} روی پست شما نظر گذاشت",
                notif_type="comment",
            )
            return redirect(post.get_absolute_url())


@login_required
def comment_edit(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if not (request.user == comment.author or request.user.is_staff):
        messages.error(request, "دسترسی ندارید.")
        return redirect("blog:post_detail", slug=comment.post.slug)

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, "نظر به‌روزرسانی شد.")
            return redirect("blog:post_detail", slug=comment.post.slug)
    else:
        form = CommentForm(instance=comment)
    return render(request, "blog/comment_form.html", {"form": form, "comment": comment})


@login_required
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if not (request.user == comment.author or request.user.is_staff):
        messages.error(request, "دسترسی ندارید.")
        return redirect("blog:post_detail", slug=comment.post.slug)
    if request.method == "POST":
        post_slug = comment.post.slug
        comment.delete()
        messages.success(request, "نظر حذف شد.")
        return redirect("blog:post_detail", slug=post_slug)
    return render(request, "blog/comment_confirm_delete.html", {"comment": comment})


def tagged_posts(request, slug=None):
    """نمایش پست‌ها بر اساس تگ انتخاب‌شده"""
    tag = get_object_or_404(Tag, slug=slug)
    posts = Post.objects.filter(tags__in=[tag]).order_by("-created_at")
    return render(request, "blog/tagged_posts.html", {"posts": posts, "tag": tag})

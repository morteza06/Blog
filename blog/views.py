from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CommentForm, PostForm
from .models import Post, Tag


# جزئیات پست
def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(approved=True)
    form = CommentForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.user = request.user
        comment.save()
        return redirect("post_detail", slug=slug)
    return render(
        request,
        "blog/post_detail.html",
        {"post": post, "comments": comments, "form": form},
    )


# صفحه اصلی
def post_list(request):
    """نمایش تمام پست‌ها"""
    posts = Post.objects.filter(status="published").order_by("-created_at")
    paginator = Paginator(posts, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "blog/post_list.html", {"page_obj": page_obj})


def tagged_posts(request, slug=None):
    """نمایش پست‌ها بر اساس تگ انتخاب‌شده"""
    tag = get_object_or_404(Tag, slug=slug)
    posts = Post.objects.filter(tags__in=[tag]).order_by("-created_at")
    return render(request, "blog/tagged_posts.html", {"posts": posts, "tag": tag})


# افزودن پست جدید
@login_required
def post_create(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        form.save_m2m()
        messages.success(request, "Post created successfully")
        return redirect(post.get_absolute_url())
    return render(request, "blog/post_form.html", {"form": form})


# ویرایش پست
@login_required
def post_edit(request, slug):
    post = get_object_or_404(Post, slug=slug, author=request.user)
    form = PostForm(request.POST or None, instance=post)
    if form.is_valid():
        form.save()
        messages.info(request, "Post updated successfully.")
        return redirect(post.get_absolute_url())
    return render(request, "blog/post_form.html", {"form": form, "title": "Edit Post"})


# حذف پست
@login_required
def post_delete(request, slug):
    post = get_object_or_404(Post, slug=slug, author=request.user)
    if request.method == "POST":
        post.delete()
        messages.warning(request, "Post deleted.")
        return redirect("blog:index")
    return render(request, "blog/post_confirm_delete.html", {"post": post})

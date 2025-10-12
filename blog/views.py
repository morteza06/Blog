from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .forms import CommentForm, PostForm


def index(request):
    posts = Post.objects.filter(is_published=True)
    paginator = Paginator(posts, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "blog/index.html", {"page_obj": page_obj})


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(approved=True)
    form = CommentForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.user = request.user
        comment.save()
        return redirect("blog:post_detail", slug=slug)
    return render(request, "blog/post_detail.html", {"post": post, "comments": comments, "form": form})


@login_required
def post_create(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        form.save_m2m()
        return redirect(post.get_absolute_url())
    return render(request, "blog/post_form.html", {"form": form})
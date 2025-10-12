from django.contrib import admin
from django.urls import path, include
from blog import views as blog_views
from accounts.views import dashboard

urlpatterns = [
    path("", blog_views.index, name="home"),  # صفحه اصلی سایت → blog/index.html
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("blog/", include("blog.urls", namespace="blog")),  # اپ اصلی
    path('dashboard/', dashboard, name='dashboard'),
]

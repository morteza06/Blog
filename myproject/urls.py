from django.contrib import admin
from django.urls import path, include
from blog.views import index
from accounts.views import dashboard

urlpatterns = [
    path("", index, name="home"),  # صفحه اصلی سایت → blog/index.html
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("blog/", include("blog.urls")),  # اپ اصلی
    path('dashboard/', dashboard, name='dashboard'),
]

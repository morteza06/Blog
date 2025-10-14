from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from accounts.views import dashboard
from blog import views as blog_views

urlpatterns = [
    path("", blog_views.index, name="home"),  # صفحه اصلی سایت → blog/index.html
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("blog/", include("blog.urls", namespace="blog")),  # اپ اصلی
    path("dashboard/", dashboard, name="dashboard"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

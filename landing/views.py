from django.shortcuts import render


def index(request):
    """صفحه‌ی اصلی سایت (Landing Page)"""
    return render(request, "landing/index.html")

from django.contrib import admin
from .models import CustomUser, Post


admin.site.register(Post)
admin.site.register(CustomUser)

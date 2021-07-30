from django.contrib import admin
from .models import Course, Article, Tag, Profile


admin.site.register(Course)
admin.site.register(Article)
admin.site.register(Tag)
admin.site.register(Profile)

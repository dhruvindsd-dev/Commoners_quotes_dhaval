from django.contrib import admin
from .models import Blog_db, Submitted_articles
# Register your models here.

admin.site.register(Blog_db)
admin.site.register(Submitted_articles)

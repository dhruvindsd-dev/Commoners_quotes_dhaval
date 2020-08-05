"""comm_quotes_blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from blog.views import *
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_index),
    path('quotes', all_quotes),
    path('stories', all_stories),
    path('poems', all_poems),
    # admin functions
    # CREATE
    path("admin_handle", admin_handle),
    path('admin_handle_loged_in', admin_handle_login),
    path('create_article/<str:cata>', create_stories_and_blogs),
    path('create_quote', create_quotes),
    # EDIT AND VIEW
    path('view_articles/<int:id>', view_stories_poems),
    path('edit_article/<int:id>', edit_stories_poems),
    path('edit_quote/<int:id>', edit_quote),
    path('img_select/<int:id>', img_select),
    # DELETE
    path('article_delete/<int:id>', article_delete),
    # RANDOM USER SUBMITTED ARTICLES
    path('user_submitted_articles/', user_submit_articles),
    path('user_submitted_articles/view/<int:id>', user_submit_articles),

    # RANDOM USER ARTICLE
    path('submit_article', random_article_submission),
    path('otp_verification', otp_verification),
    path('article', article_submit),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("courses", views.courses, name="courses"),
    path("register", views.register, name="register"),
    path("login", views.login_request, name="login"),
    path("logout", views.logout_request, name="logout"),
    path("news", views.news, name="news"),
    path("user", views.userpage, name="userpage"),
    path("<article_page>", views.article, name="article"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

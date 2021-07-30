from django.shortcuts import render, redirect
from .models import Course, Article
from django.core.paginator import Paginator
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import NewUserForm, UserForm, ProfileForm
from django.shortcuts import get_object_or_404


def homepage(request):
    if request.method == "POST":
        course_id = request.POST.get('cour_pk')
        course = Course.objects.get(id=course_id)
        request.user.profile.courses.add(course)
        messages.success(request, f'{course} добавлен в список желаний')
        return redirect('homepage')
    courses = Course.objects.all()[:4]
    new_posts = Article.objects.all().order_by('-article_published')[:4]
    featured = Article.objects.all()[:2]
    most_recent = new_posts.first()
    return render(request, "main/home.html", {'courses': courses, 'most_recent': most_recent, "new_posts": new_posts, "featured": featured})


def courses(request):
    if request.method == "POST":
        course_id = request.POST.get("cour_pk")
        course = get_object_or_404(Course, id=course_id)
        request.user.profile.courses.add(course)
        messages.success(request, f'{course} Добавлен в список желаний')
        return redirect("courses")

    courses = Course.objects.all()
    paginator = Paginator(courses, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "main/courses.html", {"page_obj": page_obj})


def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Регистрация прошла успешно")
            return redirect("homepage")
        messages.error(request, "Произошла ошибка, проверьте вводимую информацию")
    form = NewUserForm
    return render(request, "main/register.html", {"form": form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"Добро пожаловать, {username}")
                return redirect("homepage")
            else:
                messages.error(request, "Неправильный логин или пароль")
        else:
            messages.error(request, "Неправильный логин или пароль")
    form = AuthenticationForm()
    return render(request, "main/login.html", {"form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "Вы успешно вышли из аккаунта")
    return redirect("homepage")


def news(request):
    news = Article.objects.all().order_by('-article_published')
    paginator = Paginator(news, 2)
    page_number = request.GET.get('page')
    news_obj = paginator.get_page(page_number)
    return render(request, "main/news.html", {"news": news_obj})


def userpage(request):
    if request.method == "POST":
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Ваш профиль успешно изменён')
        elif profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Ваш список желаний успешно обновлён')
        else:
            messages.error(request, 'Произошла ошибка :(')
        return redirect("userpage")

    user_form = UserForm(instance=request.user)
    profile_form = ProfileForm(instance=request.user.profile)
    return render(request, "main/user.html", {"user": request.user, "user_form": user_form, "profile_form": profile_form})


def article(request, article_page):
    article = get_object_or_404(Article, article_slug=article_page)
    return render(request, 'main/article.html', {"article": article})





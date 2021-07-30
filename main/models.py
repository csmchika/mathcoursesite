from django.db import models
from django.utils import timezone
from tinymce.models import HTMLField
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


class Course(models.Model):
    course_name = models.CharField(max_length=150)
    course_type = models.CharField(max_length=25, default='ЕГЭ')
    course_description = models.TextField(default='Один из курсов по математике')
    affiliate_url = models.SlugField(blank=True, null=True)
    course_image = models.ImageField(upload_to='courses_images', default='default.png')

    def __str__(self):
        return self.course_name

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Tag(models.Model):
    tag_name = models.CharField(max_length=15)
    tag_slug = models.SlugField()

    def __str__(self):
        return self.tag_name

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'


class Article(models.Model):
    article_title = models.CharField(max_length=200)
    article_published = models.DateTimeField('Дата публикации', default=timezone.now)
    article_image = models.ImageField(upload_to='news_images/')
    article_tags = models.ManyToManyField(Tag)
    article_content = HTMLField()
    article_slug = models.SlugField()

    def __str__(self):
        return self.article_title

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    courses = models.ManyToManyField(Course)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

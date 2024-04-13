from django.db import models
from django.urls import reverse


class PublishedModel(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=ScriptPost.Status.PUBLISHED)


class ScriptPost(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    title = models.CharField(max_length=255, verbose_name='Заголовок')
    slug = models.SlugField(max_length=255, db_index=True, unique=True, verbose_name='Слаг')
    content = models.TextField(verbose_name='Код')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
    about = models.TextField(null=True, verbose_name='Описание')
    is_published = models.BooleanField(choices=tuple(map(lambda x:(bool(x[0]), x[1]), Status.choices)), default=Status.DRAFT, verbose_name='Статус')

    objects = models.Manager()
    published = PublishedModel()

    cat_id = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категория')
    tags = models.ManyToManyField('TagPost', blank=True, related_name='tags', verbose_name='Тэги')
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True, blank=True, related_name='ascript', verbose_name='Автор')

    class Meta:
        verbose_name = 'Пользовательские публикации'
        verbose_name_plural = 'Пользовательские публикации'
        ordering = ['-time_create']
        indexes = [
            models.Index(fields=['-time_create']),
        ]

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=255, db_index=True, verbose_name='Название')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='Слаг')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    def __str__(self):
        return self.name


class TagPost(models.Model):
    tag = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_slug': self.slug})

    def __str__(self):
        return self.tag


class Author(models.Model):
    username = models.CharField(max_length=255, unique=True)
    sp_count = models.IntegerField(blank=True, default=0)

    def __str__(self):
        return self.username

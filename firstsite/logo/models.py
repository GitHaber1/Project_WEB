from django.db import models


class PublishedModel(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=ScriptPost.Status.PUBLISHED)


class ScriptPost(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Rough post'
        PUBLISHED = 1, 'Published'

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, db_index=True, unique=True)
    content = models.TextField()
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(choices=Status.choices, default=Status.DRAFT)

    objects = models.Manager()
    published = PublishedModel()

    class CategoryChoices(models.TextChoices):
        CATEGORY_CPP = 'C++', 'C++'
        CATEGORY_CS = 'C#', 'C#'

    category = models.CharField(max_length=50, choices=CategoryChoices.choices, default=CategoryChoices.CATEGORY_CPP)

    class Meta:
        ordering = ['-time_create']
        indexes = [
            models.Index(fields=['-time_create']),
        ]

    def __str__(self):
        return self.title

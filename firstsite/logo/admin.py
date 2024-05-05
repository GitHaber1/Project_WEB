from django.contrib import admin
from django.utils.html import format_html

from .models import ScriptPost, Category, Screenshots
from django.db.models import Q

# Register your models here.


class AuthorFilter(admin.SimpleListFilter):
    title = 'Статус автора поста'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return [
            ('beginners', 'Любители'),
            ('advanced', 'Опытные'),
            ('experts', 'Эксперты')
        ]

    def queryset(self, request, queryset):
        if self.value() == 'beginners':
            return queryset.filter(Q(author__sp_count__gte=1) & Q(author__sp_count__lt=3))
        elif self.value() == 'advanced':
            return queryset.filter(Q(author__sp_count__gte=3) & Q(author__sp_count__lt=10))
        elif self.value() == 'experts':
            return queryset.filter(author__sp_count__gte=10)


class ScreenshotsInline(admin.TabularInline):
    model = Screenshots
    extra = 1

    def get_image(self, obj):
        if obj.screenshot:
            return format_html('<img src="{}" width="100" height="100" />', obj.screenshot.url)
        return '-'

    get_image.short_description = 'Изображение'
    readonly_fields = ('get_image',)
    fields = ('screenshot', 'get_image',)


@admin.register(ScriptPost)
class ScriptPostAdmin(admin.ModelAdmin):
    fields = ['title', 'slug', 'content', 'about', 'cat_id', 'author', 'tags', 'is_published']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['tags']
    list_display = ('id', 'title', 'time_create', 'cat_id', 'is_published', 'brief_info')
    list_display_links = ('id', 'title')
    ordering = ['-time_create', 'title']
    list_editable = ('is_published', 'cat_id')
    list_per_page = 5
    actions = ['set_published', 'set_draft']
    search_fields = ['title__startswith', 'cat_id__name']
    list_filter = [AuthorFilter, 'cat_id__name', 'is_published']

    inlines = [ScreenshotsInline]

    @admin.display(description='Размер кода')
    def brief_info(self, post: ScriptPost):
        return f"Код из {len(post.content)} символов."

    @admin.action(description='Опубликовать выбранные записи')
    def set_published(self, request, queryset):
        count = queryset.update(is_published=ScriptPost.Status.PUBLISHED)
        self.message_user(request, f'Опубликовано {count} записей.')

    @admin.action(description='Снять с публикации выбранные записи')
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=ScriptPost.Status.DRAFT)
        self.message_user(request, f'Снято с публикации {count} записей.')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    list_per_page = 5

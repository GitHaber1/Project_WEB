import django.urls.converters
from django.urls import path
from logo import views, converters
from .admin import admin


urlpatterns = [
    path('', views.index, name='home'),
    path('login/', views.login, name='login'),
    # path('categories/<int:cat_id>/', views.categories, name='categories_id'),
    # path('categories/<slug:cat_slug>/', views.categories_by_slug, name='categories'),
    # path('archive/<year4:year>/', views.archive, name='archive'),
    path('about/', views.about, name='about'),
    path('info/<int:id>', views.show_additional_info, name='info'),
    path('category/<slug:cat_slug>', views.show_category, name='category'),
    path('category/<slug:cat_slug>/post/<slug:post_slug>/', views.show_post, name='show_post'),
    path('category/<slug:cat_slug>/tag/<slug:tag_slug>', views.show_tag_postlist, name='tag'),
    path('add_page/', views.add_page, name='create_post'),
    path('upload/', views.upload, name='upload')
]

admin.site.site_header = "Панель администрирования"
admin.site.index_title = "Пользовательские публикации"

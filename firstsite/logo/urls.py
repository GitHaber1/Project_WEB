import django.urls.converters
from django.urls import path
from logo import views, converters
from .admin import admin


urlpatterns = [
    path('', views.LogoIndex.as_view(), name='home'),
    path('about/', views.LogoAbout.as_view(), name='about'),
    path('info/<int:id>', views.show_additional_info, name='info'),
    path('add_page/', views.AddPage.as_view(), name='create_post'),
    path('upload/', views.upload, name='upload'),
    path('edit/<int:pk>/', views.UpdatePage.as_view(), name='edit_page'),
    path('delete/<int:pk>/', views.DeletePage.as_view(), name='delete_page'),
    path('category/<slug:cat_slug>', views.ScriptCategory.as_view(), name='category'),
    path('category/<slug:cat_slug>/post/<slug:post_slug>/', views.ShowPost.as_view(), name='show_post'),
    path('category/<slug:cat_slug>/tag/<slug:tag_slug>', views.TagPostList.as_view(), name='tag'),
]

admin.site.site_header = "Панель администрирования"
admin.site.index_title = "Пользовательские публикации"

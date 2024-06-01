import django.urls.converters
from django.urls import path
from logo import views, converters
from .admin import admin


urlpatterns = [
    path('', views.LogoIndex.as_view(), name='home'),
    path('about/', views.LogoAbout.as_view(), name='about'),
    path('add_page/', views.AddPage.as_view(), name='create_post'),
    path('edit/<int:pk>/', views.UpdatePage.as_view(), name='edit_page'),
    path('delete/<int:pk>/', views.DeletePage.as_view(), name='delete_page'),
    path('category/<slug:cat_slug>', views.ScriptCategory.as_view(), name='category'),
    path('category/<slug:cat_slug>/post/<slug:post_slug>/', views.ShowPost.as_view(), name='show_post'),
    path('category/<slug:cat_slug>/tag/<slug:tag_slug>', views.TagPostList.as_view(), name='tag'),
    path('comment/add/<int:pk>', views.AddComment.as_view(), name='add_comment'),
    path('comment/edit/<int:pk>', views.EditComment.as_view(), name='edit_comment'),
    path('comment/delete/<int:pk>', views.DeleteComment.as_view(), name='delete_comment'),
    path('post/<slug:post_slug>/like', views.LikePost.as_view(), name='like_post'),
    path('myposts/', views.ShowUserPosts.as_view(), name='show_user_posts')
]

admin.site.site_header = "Панель администрирования"
admin.site.index_title = "Пользовательские публикации"

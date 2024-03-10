import django.urls.converters
from django.urls import path
from logo import views, converters

django.urls.converters.register_converter(converters.FourDigitYearConverter, "year4")

urlpatterns = [
    path('', views.index, name='home'),
    path('login/', views.login, name='login'),
    path('categories/<int:cat_id>/', views.categories, name='categories_id'),
    path('categories/<slug:cat_slug>/', views.categories_by_slug, name='categories'),
    path('archive/<year4:year>/', views.archive, name='archive'),
    path('about/', views.about, name='about'),
    path('info/<int:id>', views.show_additional_info, name='info')
]

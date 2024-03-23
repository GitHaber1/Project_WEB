import django
import django.http
from django.shortcuts import render, get_object_or_404
from django.template.defaultfilters import slugify
from logo.models import ScriptPost
from django.urls import reverse

# Create your views here.

menu = [{'title': 'Login', 'url_name': 'login'},
            {'title': 'About', 'url_name': 'about'}]


cats_db = [
    {'id': 1, 'name': 'C++'},
    {'id': 2, 'name': 'C#'},
]


class MyClass:
 def __init__(self, a, b):
    self.a = a
    self.b = b


def index(request):
    data = {
        'title': 'This is logo',
        'menu': menu,
        'url': slugify("This is logo"),
        'float': 28.56,
        'lst': [1, 2, 'abc', True],
        'set': {1, 1, 2, 3, 2, 5},
        'dict': {'key_1': 'value_1', 'key_2':
            'value_2'},
        'obj': MyClass(10, 20),
    }

    return render(request, 'logo_temps/index.html', context=data)


def login(request):
    return django.shortcuts.HttpResponse("Login")


def categories(request, cat_id):
    return django.shortcuts.HttpResponse(f"<h1>Categories of logo</h1><p >id:{cat_id}</p>")


def categories_by_slug(request, cat_slug):
    if request.GET:
        print(request.GET)

    if request.POST:
        print(request.POST)

    return django.shortcuts.HttpResponse(f"<h1>Categories of logo</h1><p >slug:{cat_slug}</p>")


def archive(request, year):
    url_redirect = django.shortcuts.reverse('categories', args=('args', ))
    if year > 2024:
        return django.shortcuts.redirect(url_redirect)

    return django.shortcuts.HttpResponse(f"<h1>Archive by years</h1><p >{year}</p>")


def about(request):
    data_db = [
        {'id': 1, 'title': 'Creator of site', 'content': 'Email: creator@gmail.com', 'is_private': True, 'info': '+78888888888'},
        {'id': 2, 'title': 'Support team', 'content': 'Our support team, which can help you!'
                                                      '\nEmail: support_site@gmail.com', 'is_private': False, 'info':'+78888888881'}

    ]
    data = {
        'title': 'About site',
        'menu': menu,
        'contacts': data_db,
    }
    return render(request, 'logo_temps/about.html', data)


def show_post(request, cat_id, post_slug):
    post = get_object_or_404(ScriptPost, slug=post_slug)
    return render(request, 'logo_temps/show_post.html', {'post': post, 'title': 'Code', 'menu': menu})


def show_category(request, cat_id):
    if (cat_id == 1):
        title = 'C++ scripts'
        category_name = ScriptPost.CategoryChoices.CATEGORY_CPP
    elif (cat_id == 2):
        title = 'C# scripts'
        category_name = ScriptPost.CategoryChoices.CATEGORY_CS

    posts = ScriptPost.published.all().filter(category=category_name)

    data = {
        'title': title,
        'menu': menu,
        'posts': posts
    }

    for post in posts:
        post.url = reverse('show_post', args=[cat_id, post.slug])

    return render(request, 'logo_temps/script_cat.html', data)


def show_additional_info(request, id):
    return django.shortcuts.HttpResponse(f"<h1>Additional contact info with id: {id}</h1>")


def page_not_found(request, exception):
    return django.http.HttpResponseNotFound("<h1>Page not found</h1>")

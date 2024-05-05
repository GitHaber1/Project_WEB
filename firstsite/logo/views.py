import django
import django.http
import uuid
from django.shortcuts import render, get_object_or_404, redirect
from django.template.defaultfilters import slugify
from logo.models import ScriptPost, Category, TagPost, Screenshots
from django.urls import reverse
from .forms import AddPostForm, UploadFileForm, AddPostFullForm

# Create your views here.

menu = [{'title': 'Вход', 'url_name': 'login'},
        {'title': 'О сайте', 'url_name': 'about'}]


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


# def categories(request, cat_id):
#     return django.shortcuts.HttpResponse(f"<h1>Categories of logo</h1><p >id:{cat_id}</p>")


# def categories_by_slug(request, cat_slug):
#     if request.GET:
#         print(request.GET)
#
#     if request.POST:
#         print(request.POST)
#
#     return django.shortcuts.HttpResponse(f"<h1>Categories of logo</h1><p >slug:{cat_slug}</p>")


# def archive(request, year):
#     url_redirect = django.shortcuts.reverse('categories', args=('args', ))
#     if year > 2024:
#         return django.shortcuts.redirect(url_redirect)
#
#     return django.shortcuts.HttpResponse(f"<h1>Archive by years</h1><p >{year}</p>")


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


def show_post(request, cat_slug, post_slug):
    post = get_object_or_404(ScriptPost, slug=post_slug)
    return render(request, 'logo_temps/show_post.html', {'post': post, 'title': post.title, 'menu': menu, 'current_cat_slug': cat_slug})


def show_category(request, cat_slug):
    current_cat = get_object_or_404(Category, slug=cat_slug)
    title = current_cat.name
    posts = ScriptPost.published.all().filter(cat_id=current_cat.pk)

    data = {
        'title': title,
        'menu': menu,
        'posts': posts,
        'current_cat_slug': cat_slug,
    }

    for post in posts:
        post.url = reverse('show_post', args=[cat_slug, post.slug])

    return render(request, 'logo_temps/script_cat.html', context=data)


def show_additional_info(request, id):
    return django.shortcuts.HttpResponse(f"<h1>Additional contact info with id: {id}</h1>")


def show_tag_postlist(request, cat_slug, tag_slug):
    tag = get_object_or_404(TagPost, slug=tag_slug)
    current_cat = get_object_or_404(Category, slug=cat_slug)
    posts = tag.tags.filter(is_published=ScriptPost.Status.PUBLISHED, cat_id=current_cat.pk)
    data = {
        'title': f'Tag: {tag.tag}',
        'menu': menu,
        'posts': posts,
        'current_cat_slug': cat_slug,
    }

    for post in posts:
        post.url = reverse('show_post', args=[cat_slug, post.slug])

    return render(request, 'logo_temps/script_cat.html', context=data)


def add_page(request):
    if request.method == 'POST':
        form = AddPostFullForm(request.POST, request.FILES)
        if form.is_valid():
            print(form.cleaned_data)
            try:
                # Потом здесь реализовать добавление автора
                post = form.save(commit=False)
                post.save()

                files = request.FILES.getlist('screenshot')

                for file in files:
                    screen = Screenshots(screenshot=file, post=post)
                    screen.save()
                    post.screenshot.add(screen)

                return redirect('home')
            except Exception as e:
                print(f"Ошибка при сохранении поста: {e}")
                form.add_error(None, 'Не удалось добавить пост')
    else:
        form = AddPostFullForm()
    return render(request, 'logo_temps/add_page.html', {'menu': menu, 'title': 'Добавление статьи', 'form': form})


def handle_uploaded_file(f):
    name = f.name
    ext = ''

    if '.' in name:
        ext = name[name.rindex('.'):]
        name = name[:name.rindex('.')]

    suffix = str(uuid.uuid4())

    with open(f"uploads/{name}_{suffix}{ext}", "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def upload(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(form.cleaned_data['file'])
    else:
        form = UploadFileForm()

    return render(request, 'logo_temps/upload.html', {'title': 'Загрузка файлов', 'menu': menu, 'form': form})


def page_not_found(request, exception):
    return django.http.HttpResponseNotFound("<h1>Page not found</h1>")

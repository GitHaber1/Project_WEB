import django
import django.http
import uuid

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import View
from .utils import DataMixin
from django.core.paginator import Paginator
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView, UpdateView, DeleteView
from django.core.files.storage import default_storage
from django.shortcuts import render, get_object_or_404, redirect
from django.template.defaultfilters import slugify
from logo.models import ScriptPost, Category, TagPost, Screenshots
from django.urls import reverse, reverse_lazy
from .forms import AddPostForm, UploadFileForm, AddPostFullForm

# Create your views here.


class LogoIndex(DataMixin, ListView):
    model = ScriptPost
    template_name = 'logo_temps/index.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        return self.get_mixin_context(super().get_context_data(**kwargs), title='This is logo')


class LogoAbout(DataMixin, ListView):
    model = ScriptPost
    template_name = 'logo_temps/about.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        data_db = [
            {'id': 1, 'title': 'Creator of site', 'content': 'Email: creator@gmail.com', 'is_private': True,
             'info': '+78888888888'},
            {'id': 2, 'title': 'Support team', 'content': 'Our support team, which can help you!'
                                                          '\nEmail: support_site@gmail.com', 'is_private': False,
             'info': '+78888888881'}
        ]
        return self.get_mixin_context(super().get_context_data(**kwargs), title='О сайте', contacts=data_db)


class ShowPost(DataMixin, DetailView):
    model = ScriptPost
    template_name = 'logo_temps/show_post.html'
    context_object_name = 'post'
    slug_url_kwarg = 'post_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = context['post']
        return self.get_mixin_context(context, title=post.title, current_cat_slug=self.kwargs.get('cat_slug'))

    def get_object(self, queryset=None):
        return get_object_or_404(ScriptPost, slug=self.kwargs[self.slug_url_kwarg])


class ScriptCategory(DataMixin, ListView):
    allow_empty = True
    template_name = 'logo_temps/script_cat.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat_slug = self.kwargs.get('cat_slug')
        current_cat = get_object_or_404(Category, slug=cat_slug)

        for post in context['posts']:
            post.url = reverse('show_post', args=[cat_slug, post.slug])

        return self.get_mixin_context(context, title=current_cat.name, current_cat_slug=cat_slug)

    def get_queryset(self):
        return ScriptPost.published.filter(cat_id__slug=self.kwargs['cat_slug']).select_related('cat_id')


@login_required
def show_additional_info(request, id):
    return django.shortcuts.HttpResponse(f"<h1>Additional contact info with id: {id}</h1>")


class TagPostList(DataMixin, ListView):
    template_name = 'logo_temps/script_cat.html'
    context_object_name = 'posts'
    allow_empty = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_slug = self.kwargs.get('tag_slug')
        cat_slug = self.kwargs.get('cat_slug')
        tag = get_object_or_404(TagPost, slug=tag_slug)

        for post in context['posts']:
            post.url = reverse('show_post', args=[cat_slug, post.slug])

        return self.get_mixin_context(context, title=tag.tag, current_cat_slug=cat_slug)

    def get_queryset(self):
        return ScriptPost.published.filter(tags__slug=self.kwargs['tag_slug'],
                                           cat_id__slug=self.kwargs['cat_slug']).select_related('cat_id')


class AddPage(LoginRequiredMixin, PermissionRequiredMixin, DataMixin, CreateView):
    model = ScriptPost
    form_class = AddPostFullForm
    permission_required = 'logo.add_scriptpost'
    template_name = 'logo_temps/add_page.html'
    success_url = reverse_lazy('home')
    title_page = 'Добавление записи'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            try:
                post = form.save(commit=False)
                post.author = self.request.user
                post.save()

                tags = form.cleaned_data.get('tags')
                if tags:
                    post.tags.set(tags)

                files = request.FILES.getlist('screenshot')
                for file in files:
                    screen = Screenshots(screenshot=file, post=post)
                    screen.save()
                    post.screenshot.add(screen)

                return redirect(self.success_url)
            except Exception as e:
                print(f"Ошибка при сохранении поста: {e}")
                form.add_error(None, 'Не удалось добавить пост')

        return render(request, self.template_name, {'form': form, **self.extra_context})

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form, **self.extra_context})


class UpdatePage(LoginRequiredMixin, PermissionRequiredMixin, DataMixin, UpdateView):
    model = ScriptPost
    form_class = AddPostFullForm
    permission_required = 'logo.change_scriptpost'
    template_name = 'logo_temps/add_page.html'
    success_url = reverse_lazy('home')
    title_page = 'Добавление записи'

    def get_object(self, queryset=None):
        post_id = self.kwargs.get('pk')
        return get_object_or_404(ScriptPost, pk=post_id)

    def post(self, request, *args, **kwargs):
        post = self.get_object()
        form = self.form_class(request.POST, request.FILES, instance=post)
        if form.is_valid():
            try:
                post = form.save(commit=False)
                post.author = self.request.user
                post.save()

                tags = form.cleaned_data.get('tags')
                if tags:
                    post.tags.set(tags)

                new_files = request.FILES.getlist('screenshot')
                old_files = post.screenshot.all()

                for old_file in old_files:
                    if old_file.screenshot not in new_files:
                        default_storage.delete(old_file.screenshot.path)
                        old_file.delete()

                for file in new_files:
                    if file not in [old_file.screenshot for old_file in old_files]:
                        screen = Screenshots(screenshot=file, post=post)
                        screen.save()
                        post.screenshot.add(screen)

                return redirect(self.success_url)
            except Exception as e:
                print(f"Ошибка при обновлении поста: {e}")
                form.add_error(None, 'Не удалось обновить пост')

        return render(request, self.template_name, {'form': form, **self.extra_context})

    def get(self, request, *args, **kwargs):
        post = self.get_object()
        form = self.form_class(instance=post)
        return render(request, self.template_name, {'form': form, **self.extra_context})


class DeletePage(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = ScriptPost
    template_name = 'logo_temps/confirm_delete.html'
    permission_required = 'logo.delete_scriptpost'
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        post_id = self.kwargs.get('pk')
        return get_object_or_404(ScriptPost, pk=post_id)

    def delete(self, request, *args, **kwargs):
        post = self.get_object()

        screenshots = post.screenshot.all()
        for screenshot in screenshots:
            screenshot.screenshot.delete()
            screenshot.delete()

        return super().delete(request, *args, **kwargs)


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

    return render(request, 'logo_temps/upload.html', {'title': 'Загрузка файлов', 'form': form})


def page_not_found(request, exception):
    return django.http.HttpResponseNotFound("<h1>Page not found</h1>")

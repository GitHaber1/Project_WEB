import django
import django.http

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .utils import DataMixin, IsOwnerMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.core.files.storage import default_storage
from django.shortcuts import render, get_object_or_404, redirect
from logo.models import ScriptPost, Category, TagPost, Screenshots, Comment, Like
from django.urls import reverse, reverse_lazy
from .forms import AddPostFullForm, CommentForm

# Create your views here.


class LogoIndex(DataMixin, ListView):
    model = ScriptPost
    template_name = 'logo_temps/index.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        return self.get_mixin_context(super().get_context_data(**kwargs), title='Coders` Hub')


class LogoAbout(DataMixin, ListView):
    model = ScriptPost
    template_name = 'logo_temps/about.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        data_db = [
            {'id': 1, 'title': 'Creator of site', 'content': 'Email: creator@gmail.com', 'is_private': True,
             'info': '+78888888888'},
            {'id': 2, 'title': 'Поддержка', 'content': 'С радостью ответим на все ваши вопросы!'
                                                          '\nEmail: django.badin@yandex.ru', 'is_private': False,
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
        user_has_liked = False
        if self.request.user.is_authenticated:
            user_has_liked = Like.objects.filter(user=self.request.user, post=post).exists()
        context['user_has_liked'] = user_has_liked
        context['comment_form'] = CommentForm()
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


class UpdatePage(LoginRequiredMixin, IsOwnerMixin, PermissionRequiredMixin, DataMixin, UpdateView):
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


class DeletePage(LoginRequiredMixin, IsOwnerMixin, PermissionRequiredMixin, DeleteView):
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


class AddComment(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = ScriptPost.objects.get(pk=self.kwargs.get('pk'))
        return super().form_valid(form)

    def get_success_url(self):
        post = ScriptPost.objects.get(pk=self.object.post.pk)
        return reverse('show_post', args=[post.cat_id.slug, post.slug])


class EditComment(IsOwnerMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'logo_temps/comment_edit.html'

    def get_success_url(self):
        post = ScriptPost.objects.get(pk=self.object.post.pk)
        return reverse('show_post', args=[post.cat_id.slug, post.slug])


class DeleteComment(IsOwnerMixin, DeleteView):
    model = Comment
    template_name = 'logo_temps/comment_delete.html'

    def get_success_url(self):
        post = ScriptPost.objects.get(pk=self.object.post.pk)
        return reverse('show_post', args=[post.cat_id.slug, post.slug])


class LikePost(LoginRequiredMixin, View):
    def post(self, request, post_slug):
        post = get_object_or_404(ScriptPost, slug=post_slug)
        like, created = Like.objects.get_or_create(user=request.user, post=post)

        if not created:
            like.delete()
            post.likes_count -= 1
            post.save()
        else:
            post.likes_count += 1
            post.save()

        return redirect('show_post', post.cat_id.slug, post.slug)


class ShowUserPosts(DataMixin, ListView):
    allow_empty = True
    template_name = 'logo_temps/script_cat.html'
    context_object_name = 'posts'
    model = ScriptPost

    def get_queryset(self):
        user = self.request.user
        queryset = ScriptPost.objects.filter(author=user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        for post in context['posts']:
            post.url = reverse('show_post', args=[post.cat_id.slug, post.slug])

        return self.get_mixin_context(context, title='Посты пользователя')


def page_not_found(request, exception):
    return django.http.HttpResponseNotFound("<h1>Page not found</h1>")

from django.core.exceptions import PermissionDenied

menu = [{'title': 'Написать пост', 'url_name': 'create_post'},
        {'title': 'О сайте', 'url_name': 'about'}]


class DataMixin:
    paginate_by = 4
    title_page = None
    extra_context = {}

    def __init__(self):
        if self.title_page:
            self.extra_context['title'] = self.title_page

    def get_mixin_context(self, context, **kwargs):
        if self.title_page:
            context['title'] = self.title_page

        context.update(kwargs)
        return context


class IsOwnerMixin(object):
    permission_denied_message = "Вы не является владельцем этой публикации и не можете её редактирвать!"

    def dispatch(self, request, *args, **kwargs):
        if (self.get_object().author != request.user and not request.user.is_superuser):
            raise PermissionDenied(self.get_permission_denied_message())
        return super().dispatch(request, *args, **kwargs)

    def get_permission_denied_message(self):
        return self.permission_denied_message

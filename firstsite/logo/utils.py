menu = [{'title': 'Вход', 'url_name': 'login'},
        {'title': 'Написать пост', 'url_name': 'create_post'},
        {'title': 'О сайте', 'url_name': 'about'}]


class DataMixin:
    paginate_by = 4
    title_page = None
    extra_context = {}

    def __init__(self):
        if self.title_page:
            self.extra_context['title'] = self.title_page

        if 'menu' not in self.extra_context:
            self.extra_context['menu'] = menu

    def get_mixin_context(self, context, **kwargs):
        if self.title_page:
            context['title'] = self.title_page

        context['menu'] = menu
        context.update(kwargs)
        return context


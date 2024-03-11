from django import template
import logo.views as views


register = template.Library()


@register.simple_tag()
def get_categories():
    return views.cats_db


@register.inclusion_tag('logo_temps/list_cats.html')
def show_categories():
    cats = views.cats_db
    return {"cats": cats}

from django import template
from logo.models import Category, TagPost
from django.db.models import Count


register = template.Library()


@register.simple_tag()
def get_categories():
    return Category.objects.all()


@register.inclusion_tag('logo_temps/list_cats.html')
def show_categories(cat_selected_id=0):
    cats = Category.objects.all()
    return {"cats": cats, "cat_selected": cat_selected_id}


@register.inclusion_tag('logo_temps/list_tags.html')
def show_all_tags(cat_slug=None):
    tags = TagPost.objects.filter(tags__cat_id__slug=cat_slug).annotate(total=Count("tags")).filter(total__gt=0)
    return {"tags": tags, "current_cat_slug": cat_slug}

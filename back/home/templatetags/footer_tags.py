from django import template
from home.snippets import Footer as FooterModel

register = template.Library()


@register.simple_tag
def get_footer():
    return FooterModel.objects.first()

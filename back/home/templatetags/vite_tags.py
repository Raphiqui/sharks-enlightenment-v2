from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def vite_dev_mode(app="default"):
    """
    Whether django-vite serves assets from the Vite dev server.
    """

    return settings.DJANGO_VITE[app].get("dev_mode", False)

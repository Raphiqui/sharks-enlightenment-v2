from django import template
from wagtail.models import Site, Locale

register = template.Library()


@register.simple_tag(takes_context=True)
def get_site_root(context):
    return Site.find_for_request(context["request"]).root_page


@register.simple_tag(takes_context=True)
def get_menu_items(context):
    """
    Retrieves the menu items based on the active language
    """

    root_page = Site.find_for_request(context["request"]).root_page
    active_language_code = Locale.get_active()
    menu_items = []

    for child_page in root_page.get_children():
        if child_page.live:
            menu_items.append(child_page.get_translation(active_language_code))

    return menu_items

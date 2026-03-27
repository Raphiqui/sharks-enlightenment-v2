from django import template
from wagtail.models import Site, Locale

register = template.Library()


@register.simple_tag(takes_context=True)
def get_site_root(context):
    active_locale = Locale.get_active()
    root_page = Site.find_for_request(context["request"]).root_page
    root_page = root_page.get_translation(active_locale)
    return root_page


@register.simple_tag(takes_context=True)
def get_menu_items(context):
    """
    Retrieves the menu items based on the active language
    """

    root_page = Site.find_for_request(context["request"]).root_page
    active_locale = Locale.get_active()
    root_page = root_page.get_translation(active_locale)

    print(root_page.__dict__)

    return (
        root_page.get_children()
        .filter(
            live=True,
            show_in_menus=True,
            locale=active_locale,
        )
        .specific()
        .select_related("locale")
    )

from django import template
from django.conf import settings
from wagtail.models import Locale, Site

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


@register.simple_tag(takes_context=True)
def get_language_links(context):
    """
    Returns the live translations of the current page (itself included),
    ordered as in settings.LANGUAGES, flagging the active one.
    """

    page = context.get("page")
    if page is None:
        return []

    active_code = Locale.get_active().language_code
    translations = {
        translation.locale.language_code: translation
        for translation in page.get_translations(inclusive=True).live().select_related("locale")
    }

    return [
        {"code": code, "page": translations[code], "is_current": code == active_code}
        for code, _ in settings.LANGUAGES
        if code in translations
    ]

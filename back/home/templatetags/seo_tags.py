import json

from django import template
from django.conf import settings
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe
from django.utils.text import Truncator
from wagtail.models import Site

from home.models import SharkPage

register = template.Library()

DESCRIPTION_MAX_LENGTH = 160


def _page_image(page):
    """
    The most representative image of a page: the shark photo, else the hero.
    """

    return getattr(page, "image", None) or getattr(page, "hero_image", None)


def _absolute(request, url):
    # Remote storages (Cloudinary) already return absolute URLs; local media doesn't.
    return request.build_absolute_uri(url) if request else url


@register.simple_tag(takes_context=True)
def meta_description(context):
    """
    The page's search description, falling back on its own content so every
    page gets a snippet instead of letting Google pick one.
    """

    page = context.get("page")
    if page is None:
        return ""

    text = page.search_description
    if not text:
        text = strip_tags(getattr(page, "description", "") or "")
    if not text:
        text = getattr(page, "hero_subtitle", "") or ""

    text = " ".join(text.split())
    return Truncator(text).chars(DESCRIPTION_MAX_LENGTH)


@register.simple_tag(takes_context=True)
def site_name(context):
    request = context.get("request")
    site = Site.find_for_request(request) if request else None
    return site.site_name if site else ""


@register.simple_tag(takes_context=True)
def canonical_url(context):
    page = context.get("page")
    return page.get_full_url(context.get("request")) if page else ""


@register.simple_tag(takes_context=True)
def get_alternate_urls(context):
    """
    hreflang alternates for every live translation of the page (itself
    included), plus x-default pointing at the default-language version.
    """

    page = context.get("page")
    if page is None:
        return []

    request = context.get("request")
    alternates = [
        {"code": translation.locale.language_code, "url": translation.get_full_url(request)}
        for translation in page.get_translations(inclusive=True).live().select_related("locale")
    ]
    if len(alternates) < 2:
        return []

    default = next(
        (alt for alt in alternates if alt["code"] == settings.LANGUAGE_CODE),
        None,
    )
    if default:
        alternates.append({"code": "x-default", "url": default["url"]})
    return alternates


@register.simple_tag(takes_context=True)
def share_image_url(context):
    """
    A 1200x630 rendition for social cards (Open Graph / Twitter).
    """

    page = context.get("page")
    image = _page_image(page) if page else None
    if image is None:
        return ""
    return _absolute(context.get("request"), image.get_rendition("fill-1200x630").url)


@register.simple_tag(takes_context=True)
def og_type(context):
    page = context.get("page")
    return "article" if page is not None and isinstance(page.specific, SharkPage) else "website"


@register.simple_tag(takes_context=True)
def structured_data(context):
    """
    JSON-LD: a WebSite on home pages, an Article on shark pages.
    """

    page = context.get("page")
    request = context.get("request")
    if page is None or request is None:
        return ""

    site = Site.find_for_request(request)
    url = page.get_full_url(request)
    language = page.locale.language_code

    # Depth 2 = directly under the tree root: the home page of each locale.
    if page.depth == 2:
        data = {
            "@context": "https://schema.org",
            "@type": "WebSite",
            "name": site.site_name if site else page.title,
            "url": url,
            "inLanguage": language,
        }
    elif isinstance(page.specific, SharkPage):
        data = {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": page.specific.name,
            "alternativeHeadline": page.specific.latin_name,
            "description": meta_description(context),
            "url": url,
            "inLanguage": language,
        }
        image = share_image_url(context)
        if image:
            data["image"] = image
        if page.last_published_at:
            data["dateModified"] = page.last_published_at.isoformat()
        if site and site.site_name:
            data["publisher"] = {"@type": "Organization", "name": site.site_name}
    else:
        return ""

    # Escape "<" so page content can never close the script tag early.
    payload = json.dumps(data, ensure_ascii=False).replace("<", "\\u003c")
    return mark_safe(f'<script type="application/ld+json">{payload}</script>')

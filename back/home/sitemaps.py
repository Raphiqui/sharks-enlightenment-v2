from django.db.models import Q
from wagtail.contrib.sitemaps import Sitemap
from wagtail.models import Page


class LocalizedSitemap(Sitemap):
    """
    Wagtail's default sitemap only walks the site's root page, which is the
    default-locale tree. Include the trees of every translation of that root.
    """

    def items(self):
        root_page = self.get_wagtail_site().root_page
        in_any_locale = Q()
        for root in root_page.get_translations(inclusive=True):
            in_any_locale |= Page.objects.descendant_of_q(root, inclusive=True)

        return (
            Page.objects.filter(in_any_locale)
            .live()
            .public()
            .order_by("path")
            .defer_streamfields()
            .specific()
        )

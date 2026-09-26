from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import TemplateView
from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.contrib.sitemaps.views import sitemap
from wagtail.documents import urls as wagtaildocs_urls
from wagtail.images.views.serve import ServeView

from home.sitemaps import LocalizedSitemap
from search import views as search_views

from .api import api

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("api/", api.urls),
    path("sitemap.xml", sitemap, {"sitemaps": {"pages": LocalizedSitemap}}),
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
    ),
    re_path(
        r"^images/([^/]*)/(\d*)/([^/]*)/[^/]*$", ServeView.as_view(), name="wagtailimages_serve"
    ),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    from django.http import Http404
    from django.views import defaults

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    # Preview the error pages (e.g. /fr/404/), which DEBUG otherwise replaces
    # with debug pages. Language-prefixed so LocaleMiddleware leaves them alone.
    urlpatterns += i18n_patterns(
        path("404/", defaults.page_not_found, {"exception": Http404()}),
        path("500/", defaults.server_error),
    )

# These paths are translatable so will be given a language prefix (eg, '/en', '/fr')
urlpatterns = urlpatterns + i18n_patterns(
    path("search/", search_views.search, name="search"),
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    path("", include(wagtail_urls)),
    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    path("pages/", include(wagtail_urls)),
)

from django.db import models

from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from django.utils.translation import gettext_lazy as _
from wagtail_localize.fields import TranslatableField


class HomePage(Page):
    body = RichTextField(_("Body"), blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]

    translatable_fields = [
        TranslatableField("body"),
    ]


class AboutPage(Page):

    parent_page_types = ["home.HomePage"]

    body = RichTextField(_("Body"), blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("body")
    ]

    translatable_fields = [
        TranslatableField("body")
    ]


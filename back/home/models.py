from django.db import models

from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from django.utils.translation import gettext_lazy as _
from wagtail_localize.fields import TranslatableField
from wagtail.images import get_image_model_string
from wagtail.blocks import (
    CharBlock,
    StructBlock,
)
from wagtail.fields import StreamField
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock

class HomePage(Page):
    body = RichTextField(_("Body"), blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]

    translatable_fields = [
        TranslatableField("body"),
    ]

class SharkThumbnail(StructBlock):

    name = CharBlock(help_text=_("Name of the shark"), required=True, label=_(""))

    image = ImageChooserBlock(
        required=True,
        help_text=_("Image of the shark"),
        label=_("Image"),
    )

    class Meta:
        template = "sharks/thumbnail.html"

    parent_page_types = ["home.HomePage"]

    body = RichTextField(_("Body"), blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("body")
    ]

    translatable_fields = [
        TranslatableField("body")
    ]


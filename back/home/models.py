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


class SharksPage(Page):
    """
    Page to display of the different type of sharks.
    """

    parent_page_types = ["home.HomePage"]
    subpage_types = []

    sharks = StreamField(
        [("shark_list", blocks.ListBlock(SharkThumbnail()))],
        blank=True,
        use_json_field=True,
        max_num=1,
    )

    content_panels = Page.content_panels + [
        FieldPanel("sharks"),
    ]

    translatable_fields = [
        TranslatableField("sharks")
    ]


class AboutPage(Page):

    parent_page_types = ["home.HomePage"]
    subpage_types = []
    
    body = RichTextField(_("Body"), blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("body")
    ]

    translatable_fields = [
        TranslatableField("body")
    ]


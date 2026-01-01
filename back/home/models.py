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

# International Union for Conservation of Nature
IUCN_STATUS = [
    ("extinct", _("extinct")),
    ("extinct in the wild", _("extinct in the wild")),
    ("critical endangered", _("critical endangered")),
    ("endangered", _("endangered")),
    ("vulnerable", _("vulnerable")),
    ("near threatened", _("near threatened")),
    ("least concern", ("least concern"))
]

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

    shark_page = blocks.PageChooserBlock(
        page_type='home.SharkPage',
        required=True,
        label=_("Shark Detail Page")
    )

    class Meta:
        template = "sharks/thumbnail.html"


class SharksPage(Page):
    """
    Page to display of the different type of sharks.
    """

    parent_page_types = ["home.HomePage"]
    subpage_types = ["home.SharkPage"]

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


class SharkPage(Page):

    parent_page_types = ["home.SharksPage"]
    subpage_types = []

    name = models.CharField(_("Name of the shark"), max_length=255)

    latin_name = models.CharField(_("Latin name"), max_length=255)
   
    image = ImageChooserBlock(
        required=True,
        help_text=_("Image of the shark"),
        label=_("Image"),
    )

    size = models.CharField(_("Size"), max_length=255)

    conservation_status = models.CharField(
        _("Conservation status"),
        max_length=100,
        choices=IUCN_STATUS,
        default=IUCN_STATUS[0],
    )

    description = RichTextField(_("Description"), blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("name"),
        FieldPanel("latin_name"),
    ]

    translatable_fields = [
        TranslatableField("name")
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


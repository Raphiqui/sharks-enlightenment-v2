from django.db import models

from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from django.utils.translation import gettext_lazy as _
from wagtail_localize.fields import TranslatableField
from wagtail.images import get_image_model_string
from wagtail.blocks import CharBlock, StructBlock, BooleanBlock, StreamBlock, ListBlock
from wagtail.fields import StreamField
from wagtail.images import get_image_model_string
from .snippets import CallToAction
from .blocks import Heading, SharkThumbnail, CardGrid

# International Union for Conservation of Nature
IUCN_STATUS = [
    ("extinct", _("extinct")),
    ("extinct in the wild", _("extinct in the wild")),
    ("critical endangered", _("critical endangered")),
    ("endangered", _("endangered")),
    ("vulnerable", _("vulnerable")),
    ("near threatened", _("near threatened")),
    ("least concern", ("least concern")),
]


class HeroMixin(Page):
    """
    Mixin for the hero section of all pages, if a page has a hero it'll be displayed
    """

    hero_image = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text=_("Image of the hero"),
        verbose_name=_("Image"),
    )

    hero_bubble_text = models.CharField(
        _("Text wrapped into a blue bubble"), max_length=255, blank=True, null=True
    )

    hero_title_white = models.CharField(
        _("Title of the page, white part"), max_length=255, blank=True, null=True
    )

    hero_title_blue = models.CharField(
        _("Title of the page, blue part"), max_length=255, blank=True, null=True
    )

    hero_subtitle = models.CharField(
        _("Subtitle of the page"), max_length=255, blank=True, null=True
    )

    hero_cta = models.ForeignKey(
        CallToAction,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text=_("Call to action button for the hero"),
        verbose_name=_("CTA"),
    )

    promote_panels = Page.promote_panels + [
        MultiFieldPanel(
            [
                FieldPanel("hero_image"),
                FieldPanel("hero_bubble_text"),
                FieldPanel("hero_title_white"),
                FieldPanel("hero_title_blue"),
                FieldPanel("hero_subtitle"),
                FieldPanel("hero_cta"),
            ],
            heading="Hero section",
        ),
    ]

    class Meta:
        abstract = True


class HomePage(HeroMixin):
    body = StreamField(
        [("heading", Heading()), ("card_grid", CardGrid())],
        blank=True,
        null=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]


class _QuizResponseBlock(StructBlock):

    response = CharBlock(help_text=_(""), required=True, label=_("Response"))

    is_correct = BooleanBlock(help_text=_("Is correct"), required=False)


class QuestionList(StructBlock):

    question = CharBlock(help_text=_("Question"), required=True, label=_(""))

    responses = StreamBlock(
        [("response", _QuizResponseBlock())],
        label=_("Possible answers"),
        required=True,
    )

    answer = CharBlock(help_text=_(""), required=True, label=_("Correct answer"))


class SharksPage(HeroMixin):
    """
    Page to display of the different type of sharks.
    """

    parent_page_types = ["home.HomePage"]
    subpage_types = ["home.SharkPage"]

    sharks = StreamField(
        [("shark_thumbnails", SharkThumbnail())],
        blank=True,
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("sharks"),
    ]

    translatable_fields = [TranslatableField("sharks")]


class SharkPage(Page):

    parent_page_types = ["home.SharksPage"]
    subpage_types = []

    name = models.CharField(_("Name of the shark"), max_length=255)

    latin_name = models.CharField(_("Latin name"), max_length=255)

    image = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text=_("Image of the shark"),
        verbose_name=_("Image"),
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
        FieldPanel("image"),
        FieldPanel("size"),
        FieldPanel("conservation_status"),
        FieldPanel("description"),
    ]

    translatable_fields = [
        TranslatableField("name"),
        TranslatableField("size"),
        TranslatableField("description"),
    ]


class QuizPage(HeroMixin):

    parent_page_types = ["home.HomePage"]
    subpage_types = []

    quiz = StreamField(
        [("question_list", ListBlock(QuestionList()))],
        blank=True,
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("quiz"),
    ]


class AboutPage(HeroMixin):

    parent_page_types = ["home.HomePage"]
    subpage_types = []

    body = RichTextField(_("Body"), blank=True)

    content_panels = Page.content_panels + [FieldPanel("body")]

    translatable_fields = [TranslatableField("body")]

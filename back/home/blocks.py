from django.utils.translation import gettext_lazy as _
from wagtail.blocks import (
    BooleanBlock,
    CharBlock,
    ListBlock,
    PageChooserBlock,
    StreamBlock,
    StructBlock,
    TextBlock,
    URLBlock,
)
from wagtail.images.blocks import ImageChooserBlock


class SharkThumbnail(StructBlock):
    name = CharBlock(help_text=_("Name of the shark"), required=True, label=_(""))

    image = ImageChooserBlock(
        required=True,
        help_text=_("Image of the shark"),
        label=_("Image"),
    )

    shark_page = PageChooserBlock(
        page_type="home.SharkPage", required=True, label=_("Shark Detail Page")
    )

    class Meta:
        template = "sharks/thumbnail.html"


class Heading(StructBlock):
    title = CharBlock(label=_("Title"))
    subtitle = CharBlock(label=_("Subtitle"), required=False)
    eyebrow = CharBlock(
        label=_("Eyebrow"),
        help_text=_("Small blue text above the main title"),
        required=False,
    )

    def __str__(self):
        return self.title

    class Meta:
        icon = "h1"
        verbose_name = _("Heading")
        verbose_name_plural = _("Headings")
        template = "blocks/section_header.html"
        form_classname = "heading-block"


class _Card(StructBlock):
    title = CharBlock(label=_("Title"), required=True)
    subtitle = CharBlock(label=_("Subtitle"), required=False)
    link = PageChooserBlock(required=True, label=_(""))
    click_label = CharBlock(label=_(""), required=False)

    class Meta:
        icon = "pilcrow"
        template = "blocks/card.html"


class CardGrid(StructBlock):
    cards = StreamBlock(
        [("card", _Card())],
        label=_("Cards"),
        required=True,
    )

    class Meta:
        icon = "pilcrow"
        verbose_name = _("Card Grid")
        verbose_name_plural = _("Cards Grid")
        template = "blocks/card-grid.html"
        form_classname = "card-grid-block"


class _SharkFact(StructBlock):
    highlight = CharBlock(
        label=_("Key figure"),
        help_text=_("Short and punchy, e.g. '400+', '1 in 3.7M' or 'Dermal denticles'"),
        max_length=40,
        required=True,
    )
    caption = CharBlock(
        label=_("Caption"),
        help_text=_("What the key figure is about, e.g. 'known shark species'"),
        required=False,
    )
    description = TextBlock(
        label=_("Description"),
        help_text=_("Revealed when the card is hovered or focused"),
        required=False,
    )
    image = ImageChooserBlock(label=_("Image"), required=False)
    source = URLBlock(label=_("Source"), required=False)
    wide = BooleanBlock(
        label=_("Wide card"),
        help_text=_("Make the card span two columns to put the fact forward"),
        required=False,
    )

    class Meta:
        icon = "pick"
        label = _("Fact")


class SharkFacts(StructBlock):
    facts = ListBlock(_SharkFact(), label=_("Facts"), min_num=1)

    class Meta:
        icon = "list-ul"
        verbose_name = _("Shark facts")
        template = "blocks/shark_facts.html"


class Anatomy(StructBlock):
    title = CharBlock(label=_("Title"), required=True)

    image = ImageChooserBlock(
        required=True,
        label=_("Image"),
    )

    class Meta:
        template = "blocks/anatomy.html"

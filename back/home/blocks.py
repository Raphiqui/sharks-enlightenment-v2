from wagtail.snippets.blocks import SnippetChooserBlock
from wagtail.images.blocks import ImageChooserBlock
from django.utils.translation import gettext_lazy as _
from wagtail.blocks import CharBlock, StructBlock, PageChooserBlock


class SectionHeaderBlock(SnippetChooserBlock):
    class Meta:
        template = "blocks/section_header.html"
        icon = "title"


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

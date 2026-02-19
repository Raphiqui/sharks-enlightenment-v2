from wagtail.snippets.models import register_snippet
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.models import Page
from django.db import models
from django.utils.translation import gettext_lazy as _


@register_snippet
class CallToAction(models.Model):
    label = models.CharField(_("Label"), max_length=255)
    page = models.ForeignKey(
        Page,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text=_("Internal page this CTA links to"),
        verbose_name=_("Page"),
    )
    external_url = models.URLField(
        _("External URL"),
        blank=True,
        help_text=_("Use this if linking to an external site instead of a page"),
    )

    panels = [
        FieldPanel("label"),
        MultiFieldPanel(
            [FieldPanel("page"), FieldPanel("external_url")],
            heading="Link (use one or the other)",
        ),
    ]

    def __str__(self):
        return self.label

    @property
    def url(self):
        if self.page:
            return self.page.url
        return self.external_url

    class Meta:
        verbose_name = _("Call to Action")
        verbose_name_plural = _("Calls to Action")


@register_snippet
class SectionHeader(models.Model):
    title = models.CharField(_("Title"), max_length=255)
    subtitle = models.CharField(_("Subtitle"), max_length=255, blank=True, null=True)
    eyebrow = models.CharField(
        _("Eyebrow"),
        help_text=_("Small blue text above the main title"),
        max_length=255,
        blank=True,
        null=True,
    )

    panels = [
        FieldPanel("title"),
        FieldPanel("subtitle"),
        FieldPanel("eyebrow"),
    ]

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Section Header")
        verbose_name_plural = _("Section Headers")

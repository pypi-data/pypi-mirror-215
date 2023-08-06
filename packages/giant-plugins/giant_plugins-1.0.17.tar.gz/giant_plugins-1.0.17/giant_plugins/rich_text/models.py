from django.db import models
from django.utils.html import strip_tags
from django.utils.text import Truncator

from cms.models import CMSPlugin
from giant_plugins.utils import RichTextField
from mixins.models import URLMixin


class RichText(CMSPlugin, URLMixin):
    """
    Represents rich text block using wysiwyg editor
    """

    anchor_id = models.CharField(max_length=255, blank=True)
    text = RichTextField(verbose_name="Text")
    cta_text = models.CharField(
        max_length=255, blank=True, help_text="text that will be displayed across the button."
    )

    def __str__(self):
        """
        String representation of the object
        """
        return self.excerpt

    @property
    def plain_text(self):
        """
        Returns the rich text without any HTML
        """
        return strip_tags(self.text)

    @property
    def excerpt(self):
        """
        Returns an excerpt of the text in plain text
        """
        return Truncator(self.plain_text).words(num=20)

    @property
    def has_cta(self):
        return any([self.get_absolute_url, self.file])

    @property
    def get_file_or_absolute_url(self):
        return self.get_absolute_url() or self.file_url

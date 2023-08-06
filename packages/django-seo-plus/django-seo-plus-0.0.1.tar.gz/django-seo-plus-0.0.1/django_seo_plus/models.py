from django.db import models

from .meta import BaseSeoMeta


# Create your models here.

class SeoMeta(BaseSeoMeta, models.Model):
    """
    Mapped abstract SeoMeta with BaseSeoMeta class
    """

    title = models.CharField(max_length=200)
    meta_description = models.TextField(null=True, blank=True,
                                        help_text='Use maximum 120 characters')
    keywords = models.CharField(max_length=200, null=True, blank=True)
    canonical_url = models.URLField(null=True, blank=True,
                                    help_text='Leave empty if the current url is canonical curl')
    block_indexing = models.BooleanField(default=False)  # Robots tag
    author = models.CharField(max_length=60, null=True, blank=True)

    class Meta:
        abstract = True

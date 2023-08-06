from django.db import models
from django.test import TestCase

from django_seo_plus.models import BaseSeoMeta


class SeoMeta(BaseSeoMeta):
    pass


# Create your tests here.

class TestSeoPlus(TestCase):
    def setUp(self) -> None:
        meta = SeoMeta()
        meta.title = 'What is django seo plus'
        self.meta = meta

    def test_meta_title_formatter(self):
        meta_title = self.meta.get_meta_title('%s - My Site')
        self.assertEquals(meta_title, 'What is django seo plus - My Site')

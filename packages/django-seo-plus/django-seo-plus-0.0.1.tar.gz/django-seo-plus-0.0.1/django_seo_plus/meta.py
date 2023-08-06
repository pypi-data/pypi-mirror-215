from abc import ABCMeta, abstractmethod


class BaseSeoMeta:
    title = None
    meta_description = None
    keywords = None
    canonical_url = None
    block_indexing = False  # Robots tag
    author = None

    def get_meta_title(self, formatter: str = None):
        if not formatter:
            return self.title

        return formatter % self.title

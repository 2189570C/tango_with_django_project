from __future__ import unicode_literals

from django.db import models
from django.template.defaultfilters import slugify

class Category(models.Model):
    MAX_NAME_LENGTH = 128
    name = models.CharField(max_length=MAX_NAME_LENGTH, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self): # For Python 2, use __unicode__ too
        return self.name

    def __unicode__(self):
        return self.name

class Page(models.Model):
    MAX_TITLE_LENGTH = 128
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=MAX_TITLE_LENGTH)
    url = models.URLField()
    views = models.IntegerField(default=0)

    def __str__(self): # For Python 2, use __unicode__ too
        return self.title

    def __unicode__(self):
        return self.title

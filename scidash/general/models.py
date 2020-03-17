import datetime
import json
import re
import urllib.request

from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from ckeditor.fields import RichTextField


class ScidashUser(AbstractUser):
    show_instructions = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Scidash user"
        verbose_name_plural = "Scidash users"

    def __str__(self):
        return super(ScidashUser, self).__str__()


class Tag(models.Model):
    name = models.CharField(max_length=100)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return self.name


def oembedReplace(match):
    url = "http://ckeditor.iframe.ly/api/oembed?url=" + \
          re.search(r'<oembed>(.*)</oembed>', match.group()).group(1)
    req = urllib.request.Request(url,
                                 headers={"Referer": "https://scidash.org"})
    f = urllib.request.urlopen(req)
    obj = json.loads(f.read())
    return obj['html']


class ActiveContentItemManager(models.Manager):
    def get_queryset(self):
        now = datetime.datetime.now()
        return super().get_queryset().filter(
            models.Q(display_from__isnull=True) |
            models.Q(display_from__lte=now),
            models.Q(display_to__isnull=True) |
            models.Q(display_to__gte=now),
        ).order_by('content_order')


class ContentItem(models.Model):
    content_order = models.PositiveIntegerField(default=0, blank=False,
                                                null=False)
    name = models.CharField(max_length=100)
    content = RichTextField()
    display_from = models.DateTimeField(null=True, blank=True)
    display_to = models.DateTimeField(null=True, blank=True)

    objects = models.Manager()
    active_objects = ActiveContentItemManager()

    def save(self, *args, **kwargs):
        # replace the oembed tags
        p = re.compile(r'<oembed>.*?</oembed>')
        self.content = p.sub(oembedReplace, self.content)
        super().save(*args, **kwargs)

    class Meta(object):
        ordering = ['content_order']

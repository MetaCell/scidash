from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from ckeditor.fields import RichTextField


class ScidashUser(AbstractUser):
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


class ContentItem(models.Model):
    content_order = models.PositiveIntegerField(default=0, blank=False, null=False)
    name = models.CharField(max_length=100)
    content = RichTextField()
    display_from = models.DateTimeField(null=True, blank=True)
    display_to = models.DateTimeField(null=True, blank=True)

    class Meta(object):
        ordering = ['content_order']

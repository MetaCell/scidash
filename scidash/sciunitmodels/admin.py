from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline

from scidash.general.models import Tag
from scidash.sciunitmodels.models import Capability, ModelClass, ModelInstance

# Register your models here.


class TagInline(GenericStackedInline):
    model = Tag


class ModelModelAdmin(admin.ModelAdmin):
    inlines = [
        TagInline,
    ]


admin.site.register(ModelClass)
admin.site.register(ModelInstance, ModelModelAdmin)
admin.site.register(Capability)

from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline

from scidash.general.models import Tag
from scidash.sciunitmodels.models import (
    Capability, ExtraCapabilityModelThrough, ModelClass, ModelInstance
)


class TagInline(GenericStackedInline):
    model = Tag


class ModelClassAdmin(admin.ModelAdmin):
    readonly_fields = ['capabilities', 'extra_capabilities']


class ModelModelAdmin(admin.ModelAdmin):
    inlines = [
        TagInline,
    ]


admin.site.register(ModelClass, ModelClassAdmin)
admin.site.register(ModelInstance, ModelModelAdmin)
admin.site.register(Capability)
admin.site.register(ExtraCapabilityModelThrough)

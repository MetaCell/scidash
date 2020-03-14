from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.contenttypes.models import ContentType

from adminsortable2.admin import SortableAdminMixin
from scidash.general.models import ScidashUser, Tag, ContentItem


# Register your models here.

class ContentItemAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ["name", "display_from", "display_to"]
    date_hierarchy = "display_from"


admin.site.register(ScidashUser, UserAdmin)
admin.site.register(ContentType)
admin.site.register(Tag)
admin.site.register(ContentItem, ContentItemAdmin)

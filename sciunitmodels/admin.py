from django.contrib import admin
from sciunitmodels.models import ModelClass, ModelInstance, Capability

# Register your models here.

admin.site.register(ModelClass)
admin.site.register(ModelInstance)
admin.site.register(Capability)

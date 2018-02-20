from django.contrib import admin
from sciunitmodels.models import ModelClass, ModelInstance

# Register your models here.

admin.site.register(ModelClass)
admin.site.register(ModelInstance)

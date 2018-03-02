from django.contrib import admin

from sciunittests.models import Score, TestInstance, TestClass, TestSuite

# Register your models here.

admin.site.register(Score)
admin.site.register(TestInstance)
admin.site.register(TestClass)
admin.site.register(TestSuite)

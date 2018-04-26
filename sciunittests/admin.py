from django.contrib import admin

from sciunittests.models import ScoreInstance, TestInstance, TestClass, TestSuite

# Register your models here.

admin.site.register(ScoreInstance)
admin.site.register(TestInstance)
admin.site.register(TestClass)
admin.site.register(TestSuite)

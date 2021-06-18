from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline

from scidash.general.models import Tag
from scidash.sciunittests.models import (
    ScoreInstance, TestClass, TestInstance, TestSuite, ScoreClass
)

# Register your models here.

class ScoreInstanceAdmin(admin.ModelAdmin):
    list_display = ('model_instance', 'test_instance', 'status', 'test_instance')
    exclude = ('related_data',)

class TestClassModelAdmin(admin.ModelAdmin):
    search_fields = ['class_name']
    readonly_fields = [
        'observation_schema', 'test_parameters_schema', 'params_units',
        'units', 'memo'
    ]


class TestInstanceInline(admin.StackedInline):
    '''
    Stacked Inline View for TestInstance
    '''
    model = TestInstance.test_suites.through
    min_num = 0
    max_num = 20
    extra = 0


class TagInline(GenericStackedInline):
    model = Tag


class TestInstanceModelAdmin(admin.ModelAdmin):
    inlines = [
        TagInline,
    ]
    list_filter = ["tags__name"]


class TestSuiteAdmin(admin.ModelAdmin):
    inlines = [
        TestInstanceInline,
    ]


admin.site.register(TestSuite, TestSuiteAdmin)
admin.site.register(ScoreInstance, ScoreInstanceAdmin)
admin.site.register(ScoreClass)
admin.site.register(TestInstance, TestInstanceModelAdmin)
admin.site.register(TestClass, TestClassModelAdmin)

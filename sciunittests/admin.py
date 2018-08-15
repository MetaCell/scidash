from django.contrib import admin

from sciunittests.models import ScoreInstance, TestInstance, TestClass, TestSuite

# Register your models here.

class TestInstanceInline(admin.StackedInline):
    '''
    Stacked Inline View for TestInstance
    '''
    model = TestInstance.test_suites.through
    min_num = 0
    max_num = 20
    extra = 0

class TestSuiteAdmin(admin.ModelAdmin):
    inlines = [
            TestInstanceInline,
            ]


admin.site.register(TestSuite, TestSuiteAdmin)


admin.site.register(ScoreInstance)
admin.site.register(TestInstance)
admin.site.register(TestClass)

from django.contrib import admin

from scidash.logviewer.models import LogFile

# Register your models here.


class LogFileAdmin(admin.ModelAdmin):

    add_form_template = 'admin/change_form.html'

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}

        log_file = LogFile.objects.get(pk=object_id)
        file_path = log_file.path
        last_lines = log_file.rows_amount

        with open(file_path) as f:
            content = f.readlines()[-last_lines:]
            content.reverse()

        extra_context.update({'lines': content[-last_lines:]})

        return super().change_view(
            request,
            object_id,
            extra_context=extra_context,
        )


admin.site.register(LogFile, LogFileAdmin)

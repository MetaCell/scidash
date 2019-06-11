from django.conf import settings as s
from django.db import models

# Create your models here.


class LogFile(models.Model):
    path = models.FilePathField(
        path=s.BASE_DIR,
        match=r'.*\.log$',
        recursive=True,
        allow_files=True,
        allow_folders=True
    )
    name = models.CharField(max_length=200, default='Log file')
    rows_amount = models.PositiveIntegerField(default=1000)

    def __str__(self):
        return f'{self.name} from {self.path}'

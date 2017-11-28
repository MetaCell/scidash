from django.contrib.auth.models import AbstractUser


class ScidashUser(AbstractUser):

    class Meta:
        verbose_name = "Scidash user"
        verbose_name_plural = "Scidash users"

    def __str__(self):
        return super(ScidashUser, self).__str__()

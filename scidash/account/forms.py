from django.contrib.auth.forms import UserCreationForm
from scidash.general.models import ScidashUser


class ScidashUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = ScidashUser

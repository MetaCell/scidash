from django.contrib.auth import authenticate, login
from django.conf import settings
from django.shortcuts import redirect, render

from scidash.account.forms import ScidashUserCreationForm
from scidash.sciunitmodels.models import ModelInstance
from scidash.sciunittests.models import TestInstance

def signup(request):
    if request.method == 'POST':
        form = ScidashUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)

            # clone initial models and tests to the new user
            _clone_demo_models_and_tests(user)

            login(request, user)
            return redirect('index')
    else:
        form = ScidashUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


def _clone_demo_models_and_tests(user):
    demo_user_id = settings.SCIDASH_DEMO_USER_ID
    if demo_user_id:
        for mi in ModelInstance.objects.filter(owner_id=demo_user_id):
            mi.clone_to_user(user).save()

        for ti in TestInstance.objects.filter(owner_id=demo_user_id):
            ti.clone_to_user(user).save()

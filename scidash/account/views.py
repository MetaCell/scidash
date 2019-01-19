from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render

from scidash.account.forms import ScidashUserCreationForm


def signup(request):
    if request.method == 'POST':
        form = ScidashUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = ScidashUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

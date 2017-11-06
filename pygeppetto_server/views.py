from django.shortcuts import render


def index(request):
    return render(request,
            'org.geppetto.frontend/src/main/webapp/build/geppetto.vm', {})

from django.shortcuts import render


def index(request):
    context = {}
    return render(request, 'twit/index.html', context)
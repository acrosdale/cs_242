from django.shortcuts import render


def index(request):
    context = {}
    return render(request, 'twit/simple_search.html', context)
from django.shortcuts import render, redirect


def index(request):
    if request.user.is_authenticated:
        return render(request, 'litreview/index.html', context={'title': 'Accueil'})
    else:
        return redirect('login')

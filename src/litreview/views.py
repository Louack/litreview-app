from django.shortcuts import redirect


def index(request):
    if request.user.is_authenticated:
        return redirect('feed')
    else:
        return redirect('login')

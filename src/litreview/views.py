from django.shortcuts import redirect, render


def index(request):
    if request.user.is_authenticated:
        return redirect('feed')
    else:
        return redirect('login')


def error_403(request, exception):
    return render(request, 'litreview/403_error.html')


def error_404(request, exception):
    return render(request, 'litreview/404_error.html')

from django.shortcuts import redirect, render


def index(request):
    if request.user.is_authenticated:
        return redirect('feed')
    else:
        return redirect('login')


def error_403(request, exception):
    response = render(request, 'litreview/403_error.html')
    response.status_code = 403
    return response


def error_404(request, exception):
    response = render(request, 'litreview/404_error.html')
    response.status_code = 404
    return response


def error_500(request):
    response = render(request, 'litreview/404_or_500_error.html')
    response.status_code = 500
    return response

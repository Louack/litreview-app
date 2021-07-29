from django.urls import path
from .views import CustomLogin, SignUp, CustomLogout

urlpatterns = [
    path('', CustomLogin.as_view(), name='login'),
    path('signup', SignUp.as_view(), name='signup'),
    path('logout', CustomLogout.as_view(), name='logout'),
]

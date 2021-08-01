from django.urls import path
from .views import Feed

urlpatterns = [
    path('', Feed.as_view(), name='feed'),
]
from django.conf import settings
from django.urls import path
from .views import Feed, UserPosts, UserSubsManagement

urlpatterns = [
    path('', Feed.as_view(paginate_by=settings.PAGINATION), name='feed'),
    path('<str:slug>/', UserPosts.as_view(paginate_by=settings.PAGINATION), name='user-posts'),
    path('<str:slug>/follows', UserSubsManagement.as_view(), name='user-subs'),
]
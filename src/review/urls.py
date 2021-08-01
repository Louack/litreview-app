from django.urls import path
from .views import Feed
from src.litreview import settings

urlpatterns = [
    path('', Feed.as_view(paginate_by=settings.PAGINATION), name='feed'),
]
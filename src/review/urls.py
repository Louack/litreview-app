from django.conf import settings
from django.urls import path
from .views import Feed, UserPosts, UserSubsManagement, PostCreation, PostUpdate, PostDeletion

urlpatterns = [
    path('', Feed.as_view(paginate_by=settings.PAGINATION), name='feed'),
    path('<str:slug>/', UserPosts.as_view(paginate_by=settings.PAGINATION), name='user-posts'),
    path('<str:slug>/follows/', UserSubsManagement.as_view(), name='user-subs'),
    path('create/ticket/', PostCreation.as_view(post_type='ticket'), name='ticket-creation'),
    path('create/answer-review/<str:pk>/', PostCreation.as_view(post_type='review'),name='answer-review-creation'),
    path('create/direct-review/', PostCreation.as_view(post_type='double'), name='direct-review-creation'),
    path('update/ticket/<str:pk>/', PostUpdate.as_view(post_type='ticket'), name='ticket-update'),
    path('update/review/<str:pk>/', PostUpdate.as_view(post_type='review'), name='review-update'),
    path('delete/ticket/<str:pk>/', PostDeletion.as_view(post_type='ticket'), name='ticket-delete'),
    path('delete/review/<str:pk>/', PostDeletion.as_view(post_type='review'), name='review-delete'),
]
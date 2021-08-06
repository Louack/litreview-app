from django.conf import settings
from django.urls import path
from .views import Feed, UserPosts, UserSubsManagement, PostCreation, PostUpdate, PostDeletion

urlpatterns = [
    path('', Feed.as_view(paginate_by=settings.PAGINATION), name='feed'),
    path('<str:slug>/', UserPosts.as_view(paginate_by=settings.PAGINATION), name='user-posts'),
    path('<str:slug>/follows/', UserSubsManagement.as_view(), name='user-subs'),
    path('ticket/create/', PostCreation.as_view(post_type='ticket'), name='ticket-creation'),
    path('review/create/answer-review/<str:pk>/', PostCreation.as_view(post_type='review'), name='answer-review-creation'),
    path('review/create/direct-review/', PostCreation.as_view(post_type='double'), name='direct-review-creation'),
    path('ticket/update/<str:pk>/', PostUpdate.as_view(post_type='ticket'), name='ticket-update'),
    path('review/update/<str:pk>/', PostUpdate.as_view(post_type='review'), name='review-update'),
    path('ticket/delete/<str:pk>/', PostDeletion.as_view(post_type='ticket'), name='ticket-delete'),
    path('review/delete/<str:pk>/', PostDeletion.as_view(post_type='review'), name='review-delete'),
]
from itertools import chain
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView
from .models import UserFollows


class Feed(LoginRequiredMixin, TemplateView):
    template_name = 'review/feed.html'
    title = 'Flux'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        followed_users = self.get_followed_users()
        posts = self.all_posts_combined_and_sorted(followed_users)
        context['posts'] = posts
        context['title'] = self.title
        return context

    def get_followed_users(self):
        couples = UserFollows.objects.all()
        followed_users = []
        for couple in couples:
            if couple.user == self.request.user:
                followed_users.append(couple.followed_user)
        return followed_users

    def get_followed_users_tickets(self, followed_users):
        followed_users_tickets = []
        for user in followed_users:
            tickets = user.ticket_set.all()
            if tickets:
                for ticket in tickets:
                    followed_users_tickets.append(ticket)
        return followed_users_tickets

    def get_followed_users_reviews(self, followed_users):
        followed_users_reviews = []
        for user in followed_users:
            reviews = user.review_set.all()
            if reviews:
                for review in reviews:
                    followed_users_reviews.append(review)
        return followed_users_reviews

    def get_non_followers_reviews(self, user_tickets, followed_users):
        non_followers_reviews = []
        for ticket in user_tickets:
            reviews = ticket.review_set.all()
            for review in reviews:
                if review.user == self.request.user or review.user in followed_users:
                    pass
                else:
                    non_followers_reviews.append(review)
        return non_followers_reviews

    def all_posts_combined_and_sorted(self, followed_users):
        user_tickets = self.request.user.ticket_set.all()
        user_reviews = self.request.user.review_set.all()
        followed_users_tickets = self.get_followed_users_tickets(followed_users)
        followed_users_reviews = self.get_followed_users_reviews(followed_users)
        non_followers_reviews = self.get_non_followers_reviews(user_tickets, followed_users)

        posts = sorted(chain(user_tickets, followed_users_tickets, user_reviews, followed_users_reviews,
                             non_followers_reviews), key=lambda post: post.time_created, reverse=True)
        return posts

    def handle_no_permission(self):
        return redirect('index')

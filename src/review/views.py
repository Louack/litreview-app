from itertools import chain
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import CreateView, DeletionMixin, DeleteView
from .forms import SelectFollowForm, LockedFollowForm
from .models import UserFollows
from authentification.models import CustomUser


class Feed(LoginRequiredMixin, ListView):
    template_name = 'review/feed.html'
    title = 'Flux'
    context_object_name = 'posts'

    def handle_no_permission(self):
        return redirect('index')

    def get_queryset(self):
        followed_users = self.get_followed_users()
        posts = self.all_posts_combined_and_sorted(followed_users)
        return posts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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


class UserPosts(LoginRequiredMixin, SingleObjectMixin, ListView):
    template_name = 'review/posts.html'
    title = 'Mes Posts'

    def handle_no_permission(self):
        return redirect('index')

    def get_queryset(self):
        target_tickets = self.object.ticket_set.all()
        target_reviews = self.object.review_set.all()
        posts = sorted(chain(target_tickets, target_reviews), key=lambda post: post.time_created, reverse=True)
        return posts

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=CustomUser.objects.all())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        context['user'] = self.object
        context['posts'] = self.object_list
        print(context)
        return context


class UserSubscriptionsList(LoginRequiredMixin, SingleObjectMixin, ListView):
    template_name = 'review/subs.html'
    title = 'Abonnements'
    model = UserFollows

    def handle_no_permission(self):
        return redirect('index')

    def get_queryset(self):
        subs = self.get_followed_and_following_users()
        return subs

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=CustomUser.objects.all())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        context['target_user'] = self.object
        context['subs'] = self.object_list
        if self.request.user == self.object:
            subs_forms = self.get_home_subs_forms()
            context['select_form'] = subs_forms['selected_form']
            context['unfollow_forms'] = subs_forms['locked_forms']
        else:
            context['foreign_form'] = self.get_foreign_sub_form()
            for sub in context['subs']:
                if self.request.user == sub['user']:
                    context['request_user_in_subs'] = True
        return context

    def get_followed_and_following_users(self):
        couples = UserFollows.objects.all()
        subs = []
        for couple in couples:
            if couple.user == self.object:
                subs.append({'user': couple.followed_user, 'sub_type': 'is_followed_by_user'})
            if couple.followed_user == self.object:
                subs.append({'user': couple.user, 'sub_type': 'is_following_user'})
        subs = sorted(subs, key=lambda x: x['user'].username)
        return subs

    def get_home_subs_forms(self):
        couples = UserFollows.objects.all()
        home_forms = {}
        can_unfollow = []
        for couple in couples:
            if couple.user == self.request.user:
                can_unfollow.append(
                    LockedFollowForm(initial={'user': self.request.user, 'followed_user': couple.followed_user}))
        home_forms['locked_forms'] = can_unfollow
        home_forms['selected_form'] = SelectFollowForm(initial={'user': self.request.user}, user=self.object)
        return home_forms

    def get_foreign_sub_form(self):
        return LockedFollowForm(initial={'user': self.request.user, 'followed_user': self.object})


class UserSubscriptionsUpdate(LoginRequiredMixin, DeletionMixin, CreateView):
    model = UserFollows
    template_name = 'review/subs.html'
    title = 'Abonnements'
    form_classes = {'select_follow': SelectFollowForm, 'target_follow': LockedFollowForm}

    def handle_no_permission(self):
        return redirect('index')

    def get_success_url(self):
        return reverse('user-subs', args=[self.user.slug])

    def get_form(self, form_class=None):
        if 'select_follow' in self.request.POST:
            form_class = self.form_classes['select_follow']
            return form_class(self.user, **self.get_form_kwargs())
        else:
            form_class = self.form_classes['target_follow']
            return form_class(**self.get_form_kwargs())

    def post(self, request, *args, **kwargs):
        self.user = self.get_object(queryset=CustomUser.objects.all())
        if 'unfollow' in self.request.POST:
            return self.delete(self, request, *args, **kwargs)
        else:
            return super(CreateView, self).post(self, request, *args, **kwargs)

    def get_userfollows(self):
        userfollows = UserFollows.objects.filter(user_id=self.request.POST['user'],
                                                      followed_user=self.request.POST['followed_user'])
        return userfollows

    def delete(self, request, *args, **kwargs):
        userfollows = self.get_userfollows()
        success_url = self.get_success_url()
        userfollows.delete()
        return HttpResponseRedirect(success_url)


class UserSubsManagement(View):
    def get(self, request, *args, **kwargs):
        view = UserSubscriptionsList.as_view(paginate_by=settings.PAGINATION)
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = UserSubscriptionsUpdate.as_view()
        return view(request, *args, **kwargs)


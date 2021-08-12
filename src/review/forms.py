from django import forms
from .models import UserFollows, Ticket, Review
from authentification.models import CustomUser

RATING_SCALE = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]


class SelectFollowForm(forms.ModelForm):
    """
    Form to create UserFollow object. Lock the user as the request user but allow the selection of the followd user
    """
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        can_follow_users = self.get_can_follow_users(user)
        self.fields['followed_user'].choices = can_follow_users

    class Meta:
        model = UserFollows
        fields = ['user', 'followed_user']
        widgets = {'user': forms.HiddenInput()}
        labels = {'followed_user': 'Sélectionnez un utilisateur à suivre'}

    def get_can_follow_users(self, user):
        """
        generates dynamic choices list of users that can be followed
        """
        couples = UserFollows.objects.all()
        users_list = list(CustomUser.objects.all())
        users_list.remove(user)
        for couple in couples:
            if couple.user == user:
                users_list.remove(couple.followed_user)
        can_follow_list = []
        for i in range(len(users_list)):
            can_follow_list.append((users_list[i].pk, users_list[i]))
        can_follow_list = sorted(can_follow_list, key=lambda couple: couple[1].username)
        return can_follow_list


class LockedFollowForm(forms.ModelForm):
    """
    Form to create UserFollow object. Lock the user as the request user and the followed user as a target user
    """
    class Meta:
        model = UserFollows
        fields = ['user', 'followed_user']
        widgets = {'user': forms.HiddenInput(),
                   'followed_user': forms.HiddenInput()}


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        exclude = ['time_created']
        widgets = {'user': forms.HiddenInput()}


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        exclude = ['time_created']
        widgets = {'ticket': forms.HiddenInput(),
                   'user': forms.HiddenInput(),
                   'rating': forms.RadioSelect(choices=RATING_SCALE)}

from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class CustomSignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for attribute in ['password1', 'password2']:
            self.fields[attribute].help_text = None
            self.fields[attribute].show_hidden_initial = True

    class Meta:
        model = CustomUser
        fields = ['username']

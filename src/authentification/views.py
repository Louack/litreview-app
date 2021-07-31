from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from .forms import CustomSignUpForm
from .models import CustomUser


class SignUp(UserPassesTestMixin, CreateView):
    model = CustomUser
    template_name = 'authentification/auth_form.html'
    form_class = CustomSignUpForm
    title = 'Inscription'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context

    def test_func(self):
        if not self.request.user.is_authenticated:
            return True

    def handle_no_permission(self):
        return redirect('index')

    def get_success_url(self):
        return reverse('login')


class CustomLogin(UserPassesTestMixin, LoginView):
    template_name = 'authentification/auth_form.html'
    title = 'Connexion'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context

    def test_func(self):
        if not self.request.user.is_authenticated:
            return True

    def handle_no_permission(self):
        return redirect('index')

    def get_success_url(self):
        return reverse('index')


class CustomLogout(LoginRequiredMixin, LogoutView):
    template_name = 'authentification/logout.html'
    title = 'Déconnexion'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context

    def handle_no_permission(self):
        return redirect('index')

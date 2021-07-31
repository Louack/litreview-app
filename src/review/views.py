from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView


class Feed(LoginRequiredMixin, TemplateView):
    def handle_no_permission(self):
        return redirect('index')



from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Server
from datetime import datetime
import random


def create_id(name):
    name = str(name)
    id = ''
    now = datetime.now()
    current_time = now.strftime("%S%d%m%y")
    for letter in name:
        id += str(ord(letter))
    id = current_time + id[:6]
    id += str(random.randint(1000, 9999))
    id = id[::-1]
    return id


@login_required
def main_view(request):
    return render(request, 'index.html')


class CreateServerView(LoginRequiredMixin, CreateView):
    template_name = 'create_server.html'
    model = Server
    fields = ['name', 'image']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form_name = form.cleaned_data.get('name')
        form_id = create_id(form_name)
        # Check if there is existing Server with created id
        while len(Server.objects.filter(id=form_id)) > 0:
            form_id = create_id(form_name)
        form.instance.id = create_id(form_name)
        return super().form_valid(form)


class DetailServerView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    template_name = 'server_detail.html'
    model = Server

    def test_func(self):
        server = self.get_object()
        if self.request.user in server.users.all():
            return True
        return False


class UpdateServerView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = 'server_update.html'
    model = Server
    fields = ['name', 'image']

    def test_func(self):
        server = self.get_object()
        if self.request.user == server.owner:
            return True
        return False

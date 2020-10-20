from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Server
from datetime import datetime
import random
from chat.models import Channel
from django.http import HttpResponse

def create_id(name, max):
    name = str(name)
    id = ''
    now = datetime.now()
    current_time = now.strftime("%S%d%m%y")
    for letter in name:
        id += str(ord(letter))
    id = current_time + id[:6]
    id += str(random.randint(1000, max))
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
        form_id = create_id(form_name, 9999)
        # Check if there is existing Server with created id
        while len(Server.objects.filter(id=form_id)) > 0:
            form_id = create_id(form_name, 9999)
        form.instance.id = create_id(form_name, 9999)
        return super().form_valid(form)


class DetailServerView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    template_name = 'server_detail.html'
    model = Server

    def test_func(self):
        server = self.get_object()
        if self.request.user in server.users.all():
            return True
        return False
    
    def post(self, request, pk):
        name = request.POST.get("name", "")
        server = Server.objects.get(id=pk)
        if not server is None:
            channel = Channel(name=name, server=server)
            channel.save()
        return redirect("server_detail", pk)
    
    def get_context_data(self, **kwargs):
        server = Server.objects.get(id=self.kwargs['pk'])
        context = super().get_context_data(**kwargs)
        context['server'] = server
        return context
    

class UpdateServerView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = 'server_update.html'
    model = Server
    fields = ['name', 'image']

    def test_func(self):
        server = self.get_object()
        if self.request.user == server.owner:
            return True
        return False
    
    def get_context_data(self, **kwargs):
        server = Server.objects.get(id=self.kwargs['pk'])
        context = super().get_context_data(**kwargs)
        context['server'] = server
        return context

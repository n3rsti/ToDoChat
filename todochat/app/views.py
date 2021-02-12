from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, DetailView, UpdateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Server
from datetime import datetime
import random
from django.core import serializers
from chat.models import Channel
from django.http import HttpResponse
from app.forms import ServerUpdateForm, ServerCreateForm
import json
from tasks.models import Task
from django.contrib.auth.models import User

def create_id(name, max):
    name = str(name)
    id = ''
    now = datetime.now()
    current_time = now.strftime("%S%d%m%y")
    for letter in name:
        id += str(ord(letter))
    id = current_time + id[:6]
    id = str(random.randint(1000, max)) + id
    id = id[::-1]
    if id[0] == "0":
        # Id can't start with 0 in Django
        id = '1' + id[1::]
    return id

@login_required
def main_view(request):
    tasks = request.user.users_tasks.all().order_by('created')
    context = {
        "tasks_json": serializers.serialize('json', tasks)
    }
    return render(request, 'index.html', context)


class CreateServerView(LoginRequiredMixin, CreateView):
    template_name = 'create_server.html'
    model = Server
    form_class = ServerCreateForm

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form_name = form.cleaned_data.get('name')
        form_id = create_id(form_name, 9999)
        # Check if there is existing Server with created id
        while Server.objects.filter(id=form_id).count() > 0:
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
        new_channel = request.POST.get("name")
        removed_user = request.POST.get("removed_user")
        print(removed_user)
        server = Server.objects.get(id=self.kwargs['pk'])
        
        if request.POST.get("add_user"):
            user = User.objects.get(username=request.POST.get("add_user"))
            if user.profile in request.user.friends_set.all():
                server.users.add(user)
                server.save()
        elif new_channel is not None and len(new_channel) > 0 and len(new_channel) <= 20 and Channel.objects.filter(name=new_channel, server=server).first() is None:
            if not server is None:
                channel = Channel(name=new_channel, server=server)
                channel.save()
            return redirect("room", pk=server_id, room_name=new_channel)
        elif removed_user and request.user == server.owner:
           
            user = User.objects.get(username=removed_user)
            server.users.remove(user)
        return redirect("server_detail", pk)
    
    def get_context_data(self, **kwargs):
        server = Server.objects.get(id=self.kwargs['pk'])
        context = super().get_context_data(**kwargs)
        context['server'] = server
        context['heading'] = f'#{server.name}' #h1 in server_base.html
        return context
    

class UpdateServerView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = 'server_update.html'
    model = Server
    form_class = ServerUpdateForm

    def test_func(self):
        server = self.get_object()
        if self.request.user == server.owner:
            return True
        return False
    
    def get_context_data(self, **kwargs):
        server = Server.objects.get(id=self.kwargs['pk'])
        context = super().get_context_data(**kwargs)
        context['server'] = server
        context['heading'] = server.name
        return context

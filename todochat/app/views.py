from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, DetailView, UpdateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Server, ServerInvitation
from tasks.models import Task
from users.models import UsersMessage, UsersChat
from datetime import datetime
import random
import string
from django.utils import timezone
from django.core import serializers
from chat.models import Channel
from django.http import HttpResponse
from app.forms import ServerUpdateForm, ServerCreateForm
import json
from django.contrib.auth.models import User

def create_num_id(length):
    letters = string.digits
    id = ''.join(random.choice(letters) for i in range(length))
    return id

def create_random_id(length):
    letters = string.ascii_letters
    id = ''.join(random.choice(letters) for i in range(length))
    return id

@login_required
def main_view(request):
    tasks = request.user.users_tasks.all().order_by('created')
    context = {
        "tasks_json": serializers.serialize('json', tasks),
        "today_tasks": Task.filter_by_date(datetime.today(), request.user)
    }
    return render(request, 'index.html', context)


class CreateServerView(LoginRequiredMixin, CreateView):
    template_name = 'create_server.html'
    model = Server
    form_class = ServerCreateForm

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form_name = form.cleaned_data.get('name')
        form_id = create_num_id(18)
        # Check if there is existing Server with created id
        while Server.objects.filter(id=form_id).count() > 0:
            form_id = create_num_id(18)
        form.instance.id = form_id
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
        server = Server.objects.get(id=self.kwargs['pk'])
        
        if new_channel is not None and len(new_channel) > 0 and len(new_channel) <= 20 and Channel.objects.filter(name=new_channel, server=server).first() is None:
            if not server is None:
                channel = Channel(name=new_channel, server=server)
                channel.save()
            return redirect("room", pk=server_id, room_name=new_channel)
        elif removed_user and request.user == server.owner:
            user = User.objects.get(username=removed_user)
            server.users.remove(user)
        elif request.POST.get("leave_server") and request.user != server.owner:
            server.users.remove(request.user)
            return ("index")
        return redirect("server_detail", pk)
    
    def get_context_data(self, **kwargs):
        server = Server.objects.get(id=self.kwargs['pk'])
        context = super().get_context_data(**kwargs)
        context['server'] = server
        context['heading'] = f'#{server.name}' #h1 in server_base.html
        return context


def invite_server_user(request, pk, username):
    server = Server.objects.get(pk=pk)
    invited_user = User.objects.get(username=username)
    if invited_user in request.user.profile.friends.all():
        if not invited_user in server.users.all():
            invitation_id = create_random_id(10)
            invitation = ServerInvitation.objects.create(server=server, id=invitation_id, invited_user=invited_user)
            message_id = create_num_id(20)
            print(message_id)
            chat=UsersChat.objects.filter(users=request.user).get(users=invited_user)
            if not chat:
                chat = UsersChat.objects.create(id=f'{invited_user}_{request.user}')
                chat.users.add(request.user)
                chat.users.add(invited_user)
                chat.save()
            invitation_message = UsersMessage.objects.create(id=message_id,chat=chat,content=f'todochat.com/i/{invitation_id}',author=request.user)
            invitation.save()
            invitation_message.save()

    return redirect("server_detail", pk)


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


class InvitationView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = ServerInvitation

    def test_func(self):
        invitation = self.get_object()
        if self.request.user == invitation.invited_user:
            return True
        return False

    def get(self, request, pk):
        if self.test_func():
            invitation = ServerInvitation.objects.get(id=pk)
            server = invitation.server
            server.users.add(request.user)
            invitation.delete()
        return redirect("server_detail", server.id)

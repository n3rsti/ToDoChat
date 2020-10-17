from django.shortcuts import render
from app.models import Server
from django.views.generic import CreateView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from app.views import Channel


class ChannelDetailView(LoginRequiredMixin, DetailView):
    model = Channel
    template_name = 'chat/room.html'

    def get_object(self):
        return Channel.objects.filter(name=self.kwargs['room_name'], server=Server.objects.get(id=self.kwargs['pk'])).first()
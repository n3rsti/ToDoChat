from django.shortcuts import render, redirect
from app.models import Server
from django.views.generic import CreateView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from app.views import Channel, create_id
from chat.models import ChannelMessage
from django.http import HttpResponse
from django.contrib.auth.models import User

class ChannelDetailView(LoginRequiredMixin, DetailView):
    model = Channel
    template_name = 'chat/room.html'


    def get_context_data(self, **kwargs):
        channel = Channel.objects.filter(name=self.kwargs['room_name'], server=Server.objects.get(id=self.kwargs['pk'])).first()
        server = Server.objects.get(id=self.kwargs['pk'])
        messages = ChannelMessage.objects.filter(channel=channel).order_by('created')
        context = super().get_context_data(**kwargs)
        context['chat_messages'] = messages
        context['server'] = server
        return context

    def get_object(self):
        return Channel.objects.filter(name=self.kwargs['room_name'], server=Server.objects.get(id=self.kwargs['pk'])).first()

    def post(self, request, pk, room_name):
        message = request.POST.get("message")
        channel = Channel.objects.get(server=Server.objects.get(id=pk), name=room_name)
        id = create_id(message, 99999)
        author = User.objects.get(username=request.POST.get("author"))
        ChannelMessage.objects.create(id=id, channel=channel, content=message, author=author)
        return redirect("room", pk=pk, room_name=room_name)
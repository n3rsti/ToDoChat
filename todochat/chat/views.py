from django.shortcuts import redirect
from app.models import Server
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from app.views import Channel, create_num_id
from chat.models import ChannelMessage
from django.contrib.auth.models import User


class ChannelDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Channel
    template_name = 'chat/room.html'

    def test_func(self):
        user = self.request.user
        server = Server.objects.get(id=self.kwargs['pk'])
        if user in server.users.all():
            return True
        return False

    def get_context_data(self, **kwargs):
        channel = Channel.objects.filter(name=self.kwargs['room_name'],
                                         server=Server.objects.get(id=self.kwargs['pk'])).first()
        for message in channel.channelmessage_set.filter(target_users=self.request.user):
            message.target_users.remove(self.request.user)
        server = Server.objects.get(id=self.kwargs['pk'])
        messages = ChannelMessage.objects.filter(channel=channel).order_by('-created')[:100][::-1]
        context = super().get_context_data(**kwargs)
        context['chat_messages'] = messages
        context['server'] = server
        context['heading'] = f'#{channel.name}'  # h1 in server_base.html
        return context

    def get_object(self):
        return Channel.objects.filter(name=self.kwargs['room_name'],
                                      server=Server.objects.get(id=self.kwargs['pk'])).first()

    def post(self, request, pk, room_name):
        message = request.POST.get("message")
        new_channel = request.POST.get("name")
        server = Server.objects.get(id=pk)
        if message is not None:
            if len(message) == 0 or len(message) > 100:
                return redirect("room", pk=pk, room_name=room_name)
            else:
                channel = Channel.objects.get(server=Server.objects.get(id=pk), name=room_name)
                id = create_num_id(20)
                author = User.objects.get(username=request.POST.get("author"))
                ChannelMessage.objects.create(id=id, channel=channel, content=message, author=author)
                return redirect("room", pk=pk, room_name=room_name)
        elif (new_channel is not None and 0 < len(new_channel) <= 20 and
              Channel.objects.filter(name=new_channel, server=server).first() is None):
            if server is not None:
                channel = Channel(name=new_channel, server=server)
                channel.save()
            return redirect("room", pk=pk, room_name=new_channel)

        else:
            return redirect("room", pk=pk, room_name=room_name)



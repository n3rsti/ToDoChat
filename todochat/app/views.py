from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, DetailView
from .models import Server

@login_required
def main_view(request):
    user = request.user
    profile = user.profile
    servers = Server.objects.filter(users=user)

    return render(request, 'index.html', {'servers': servers})

class CreateServerView(CreateView):
    template_name = 'create_server.html'
    model = Server
    fields = ['name', 'image']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class DetailServerView(DetailView):
    template_name = 'server_detail.html'
    model = Server
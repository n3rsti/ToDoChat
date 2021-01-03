from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from tasks.models import Task
from app.models import Server
from .forms import TaskDescriptionForm
import uuid
import datetime

class TaskListView(ListView, LoginRequiredMixin, UserPassesTestMixin):
    template_name = "task_list.html"
    model = Task

    def test_func(self):
        server = self.get_object().server
        if self.request.user in server.users.all():
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        server = Server.objects.get(id=self.kwargs['server_id'])
        context['server'] = server
        context['task_list'] = Task.objects.filter(server=server).order_by('created')
        context['heading'] = 'All tasks'
        context['desc_form'] = TaskDescriptionForm
        return context
    
    def post(self, request, server_id):
        title = request.POST.get('title')
        description = request.POST.get('description')
        assignments = request.POST.getlist('assignments')
        server = Server.objects.get(id=server_id)
        server_task_id = Task.objects.filter(server=server).count() + 1
        task = Task.objects.create(task_id=server_task_id, title=title, description=description, created_by=request.user, server=server)
        if len(assignments) == 0:
            task.assigned_for.add(request.user)
        else:
            for i in range(server.users.count()):
                print(server.users.all()[i], assignments[i])
                if assignments[i] == "on":
                    task.assigned_for.add(server.users.all()[i])
        task.save()
        return redirect("server_tasks", server_id)


class TaskDetailView(DetailView, LoginRequiredMixin):
    model = Task
    template_name = "task_detail.html"
    slug_field = "id"
    slug_url_kwarg = "id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = Task.objects.get(pk=self.kwargs['id'])
        context['task'] = task
        context['server'] = Server.objects.get(id=self.kwargs['server_id'])
        context['heading'] = f'Task #{task.task_id}'
        return context
        
    def test_func(self):
        server = self.get_object().server
        if self.request.user in server.users.all():
            return True
        return False
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from tasks.models import Task
from app.models import Server
import uuid
import datetime

class TaskListView(ListView, LoginRequiredMixin):
    template_name = "task_list.html"
    model = Task

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        server = Server.objects.get(id=self.kwargs['server_id'])
        context['server'] = server
        context['task_list'] = Task.objects.filter(server=server).order_by('created')
        context['heading'] = 'All tasks'
        return context
    
    def post(self, request, server_id):
        title = request.POST.get('title')
        description = request.POST.get('description')
        assignments = request.POST.getlist('assignments')
        server = Server.objects.get(id=server_id)
        id = str(uuid.uuid4())
        while Server.objects.filter(id=id).first() is not None:
            id = str(uuid.uuid4())
        server_task_id = Task.objects.filter(server=server).count() + 1
        task = Task.objects.create(id=id, task_id=server_task_id, title=title, description=description, created_by=request.user, server=server)
        if len(assignments) == 0:
            task.assigned_for.add(request.user)
        else:
            for i in range(server.users.count()):
                print(server.users.all()[i], assignments[i])
                if assignments[i] == "on":
                    task.assigned_for.add(server.users.all()[i])
        task.save()
        return redirect("server_tasks", server_id)
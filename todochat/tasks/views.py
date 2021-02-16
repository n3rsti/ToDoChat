from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from tasks.models import Task, TaskComment, TaskStatusChange
from app.models import Server, Channel
from django.contrib.auth.models import User
from .forms import TaskDescriptionForm, TaskUpdateForm, TaskCommentForm
import uuid
import json
import datetime
from django.contrib import messages
from django.http import HttpResponseRedirect
from operator import attrgetter
from itertools import chain


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
        context['task_list'] = Task.objects.filter(
            server=server).order_by('created')
        context['heading'] = 'All tasks'
        context['desc_form'] = TaskDescriptionForm
        return context

    def post(self, request, server_id):
        title = request.POST.get('title')
        new_channel = request.POST.get("name")
        server = Server.objects.get(id=server_id)
        if title is not None:
            description = request.POST.get('description')
            assignments = request.POST.getlist('assignments')
            deadline = request.POST.get('deadline')
            server = Server.objects.get(id=server_id)
            server_task_id = Task.objects.filter(server=server).count() + 1
            task = Task.objects.create(task_id=server_task_id, title=title,
                                    description=description, author=request.user, server=server)
            if deadline != "":
                task.deadline = deadline
            if len(assignments) == 0:
                task.assigned_for.add(request.user)
            else:
                for i in range(server.users.count()):
                    if assignments[i] == "on":
                        task.assigned_for.add(server.users.all()[i])
            task.save()
            return redirect("server_tasks", server_id)
        elif new_channel is not None and len(new_channel) > 0 and len(new_channel) <= 20 and Channel.objects.filter(name=new_channel, server=server).first() is None:
            if not server is None:
                channel = Channel(name=new_channel, server=server)
                channel.save()
            return redirect("room", pk=server_id, room_name=new_channel)
        else:
            return HttpResponseRedirect(self.request.path_info)


class TaskDetailView(DetailView, LoginRequiredMixin, UserPassesTestMixin):
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
        context['comment_form'] = TaskCommentForm
        context['comment_list'] = sorted(
    chain(task.task_comments.all(), task.task_status_changes.all()),
    key=attrgetter('created'))
        return context


    def test_func(self):
        server = self.get_object().server
        if self.request.user in server.users.all():
            return True
        return False
    
    def post(self, request, server_id, id):
        new_channel = request.POST.get("name")
        server = Server.objects.get(id=server_id)
        task = Task.objects.get(id=id)
        if new_channel is not None and len(new_channel) > 0 and len(new_channel) <= 20 and Channel.objects.filter(name=new_channel, server=server).first() is None:
            if not server is None:
                channel = Channel(name=new_channel, server=server)
                channel.save()
            return redirect("room", pk=server_id, room_name=new_channel)
        elif request.POST.get("delete_task"):
            if request.user == task.author:
                task.delete()
            return redirect("server_tasks", server_id)
        elif request.POST.get("comment_task"):
            form = TaskCommentForm(request.POST)
            form.instance.task_type = "comment"
            form.instance.author = request.user
            form.instance.task = task
            if form.is_valid():
                content = form.cleaned_data.get('content')
                if len(content.replace("&nbsp;", "").replace(" ", "").replace("<p>", "").replace("</p>", "")) == 0:
                    return HttpResponseRedirect(self.request.path_info)
                form.save()
        elif request.POST.get("delete_message"):
            comment_id = request.POST.get("comment_id")
            comment = TaskComment.objects.get(id=comment_id)
            if comment.author == request.user:
                comment.delete()
        return HttpResponseRedirect(self.request.path_info)



def change_status_view(request, server_id, id):
    if request.method == "GET":
        if request.GET["status"]:
            task = Task.objects.get(id=id)
            status_list = ["approved", "open", "need_more_work", "submitted_for_review"]
            if request.GET["status"] in status_list:
                task.change_status(request.GET["status"], request.user)
    return redirect("task_detail", server_id, id)

class TaskUpdateView(UpdateView, LoginRequiredMixin, UserPassesTestMixin):
    model = Task
    template_name = "task_update.html"
    slug_field = "id"
    slug_url_kwarg = "id"
    form_class = TaskUpdateForm

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


    def post(self, request, server_id, id):
        new_channel = request.POST.get("name")
        server = Server.objects.get(id=server_id)
        if new_channel is not None and len(new_channel) > 0 and len(new_channel) <= 20 and Channel.objects.filter(name=new_channel, server=server).first() is None:
            if not server is None:
                channel = Channel(name=new_channel, server=server)
                channel.save()
            return redirect("room", pk=server_id, room_name=new_channel)
        title = request.POST.get("title")
        description = request.POST.get("description")
        task = Task.objects.get(id=id)
        task.assigned_for.clear()
        assigned_list = request.POST.get("assigned_users_list")
        print(json.loads(assigned_list))
        for user in json.loads(assigned_list):
            if User.objects.filter(username=user).first() in server.users.all():
                task.assigned_for.add(User.objects.get(username=user))
        if task.assigned_for.count() == 0:
            task.assigned_for.add(task.author)
        if len(title) <= 20:
            task.title = title
        if len(description) <= 4000:
            task.description = description
        task.save()
        return redirect("task_detail", server_id, id)


    
class FilterTaskView(ListView):
    model = Task
    template_name = "user_task_list.html"

    def get_object(self):
        return self.request.user.users_tasks.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        field_names = []
        for field_name in self.model._meta.get_fields():
            field_names.append(field_name.name)
        parameters = {field_name: value for field_name, value in self.request.GET.items() if field_name in field_names}
        context['tasks'] = self.request.user.users_tasks.filter(**parameters)
        context['taskbar_title'] = "All tasks"
        return context
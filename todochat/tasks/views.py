from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from tasks.models import Task, TaskComment
from app.models import Server, Channel
from .forms import TaskDescriptionForm, TaskUpdateForm, TaskCommentForm
import uuid
import datetime
from django.contrib import messages
from django.http import HttpResponseRedirect


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
            server = Server.objects.get(id=server_id)
            server_task_id = Task.objects.filter(server=server).count() + 1
            task = Task.objects.create(task_id=server_task_id, title=title,
                                    description=description, created_by=request.user, server=server)
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
        elif request.POST.get("delete_task"):
            if request.user == Task.objects.get(id=id).author:
                Task.objects.get(pk=id).delete()
                return redirect("server_tasks", server_id)
            else:
                return HttpResponseRedirect(self.request.path_info)
        elif request.POST.get("comment_task"):
            form = TaskCommentForm(request.POST)
            form.instance.task_type = "comment"
            form.instance.author = request.user
            form.instance.task = Task.objects.get(id=id)
            if form.is_valid():
                content = form.cleaned_data.get('content')
                if len(content.replace("&nbsp;", "").replace(" ", "").replace("<p>", "").replace("</p>", "")) == 0:
                    return HttpResponseRedirect(self.request.path_info)
                form.save()
                return HttpResponseRedirect(self.request.path_info)
            else:
                return HttpResponseRedirect(self.request.path_info)
        elif request.POST.get("delete_message"):
            print(1233)
            comment_id = request.POST.get("comment_id")
            comment = TaskComment.objects.get(id=comment_id)
            if comment.author == request.user:
                comment.delete()
            return HttpResponseRedirect(self.request.path_info)
        else:
            return HttpResponseRedirect(self.request.path_info)

    


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

    def form_valid(self, form):
        return super().form_valid(form)

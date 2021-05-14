from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseForbidden
from .models import Server, ServerInvitation
from tasks.models import Task
from users.models import UsersMessage, UsersChat
from datetime import datetime
import random
import string
from chat.models import Channel
from app.forms import ServerUpdateForm, ServerCreateForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from calendar import monthrange
from django.http import JsonResponse
from django.template.loader import render_to_string


def get_prev_and_next_month_params(month, year):
    prev_month_year = next_month_year = year
    prev_month = month - 1
    next_month = month + 1
    if prev_month == 0:  # if month is January, month - 1 would give 0
        prev_month = 12
        prev_month_year = year - 1
    elif next_month == 13:  # if month is December, month + 1 would give 13
        next_month = 1
        next_month_year = year + 1

    return f"?month={prev_month}&year={prev_month_year}", f"?month={next_month}&year={next_month_year}"


def filter_by_date(date, user):
    return Task.objects.filter(
        deadline__year=date.year,
        deadline__month=date.month,
        deadline__day=date.day,
        assigned_for=user
    )


def create_num_id(length):
    letters = string.digits[1:]
    id = ''.join(random.choice(letters) for i in range(length))
    return id


def create_random_id(length):
    letters = string.ascii_letters
    id = ''.join(random.choice(letters) for i in range(length))
    return id


def render_calendar(request):
    # Get GET parameters. If no parameters are provided, month and year are set as current date
    year = request.GET.get('year')
    month = request.GET.get('month')
    now = datetime.now()
    if year is None:
        year = now.year
    if month is None:
        month = now.month

    month = int(month)
    year = int(year)
    is_current_month = (month == now.month) and (year == now.year)
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul",
              "Aug", "Sep", "Oct", "Nov", "Dec"]

    # Get all possible values for deadline year and parse into sorted list
    # If user has tasks in years: 2008, 2013, 2015 => output: [2008, 2013, 2015]
    years = list(request.user.users_tasks.values_list('deadline__year', flat=True).distinct())
    if None in years:
        years.remove(None)
    if year not in years:
        years.append(int(year))
    years.sort()
    # Get all days in current month with existing task and parse into list
    # Example output: [1, 10, 23, 25] where each number is representing day in month where task has its deadline
    task_days = list(request.user.users_tasks.filter(deadline__year=year, deadline__month=month).
                     values_list('deadline__day', flat=True).distinct())

    """
    Create list of calendar days to be rendered
    """
    # first_weekday contains weekday of first day in month => 1-Monday, 7-Sunday
    first_weekday = datetime(year, month, 1).weekday() + 1

    current_month_days_count = monthrange(year, month)[1]
    """
    Create blank tile for every day from previous month (x on scheme) and concatenate them with list of
    actual days to be rendered

    M, T, W etc. - weekdays
    Example: month starts at Thursday:
    M  T  W  T  F  S  S
    x  x  x  1  2  3  4
    """
    total_days = [None for x in range(1, first_weekday)] + list(range(1, current_month_days_count + 1))

    context = {
        "year": int(year),
        "month": int(month),
        "months": months,
        "years": years,
        "task_days": task_days,
        "render_days": total_days,
        "is_current_month": is_current_month,
        "current_day": now.day,
        "user": request.user,
    }
    html = render_to_string(
        template_name="calendar.html",
        context=context
    )
    if request.is_ajax():
        data_dict = {"html_from_view": html}
        return JsonResponse(data=data_dict, safe=False)
    return html


@login_required
def main_view(request):
    # Get GET parameters. If no parameters are provided, month and year are set as current date
    year = request.GET.get('year')
    month = request.GET.get('month')
    now = datetime.now()
    if year is None:
        year = now.year
    if month is None:
        month = now.month
    
    month = int(month)
    year = int(year)
    prev_month, next_month = get_prev_and_next_month_params(month, year)
    context = {
        "today_tasks": request.user.users_tasks.order_by("-deadline")[:10],
        "calendar": render_calendar(request),
        "prev_month_params": prev_month,
        "next_month_params": next_month,
        # variables used in calendar
        "month": month,
        "year": year
    }
    return render(request, 'index.html', context)


class CreateServerView(LoginRequiredMixin, CreateView):
    template_name = 'create_server.html'
    model = Server
    form_class = ServerCreateForm

    def form_valid(self, form):
        form.instance.owner = self.request.user
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
        invited_user = request.POST.get("invited_user")
        server = Server.objects.get(id=self.kwargs['pk'])

        if (new_channel is not None and 0 < len(new_channel) <= 20 and
                Channel.objects.filter(name=new_channel, server=server).first() is None):
            if server is not None:
                channel = Channel(name=new_channel, server=server)
                channel.save()
            return redirect("room", pk=server.id, room_name=new_channel)
        elif removed_user and request.user == server.owner:
            user = User.objects.get(username=removed_user)
            server.users.remove(user)
        elif request.POST.get("leave_server") and request.user != server.owner:
            server.users.remove(request.user)
            return redirect("index")
        elif invited_user:
            return redirect("invite_server_user", pk, invited_user)
        return redirect("server_detail", pk)

    def get_context_data(self, **kwargs):
        server = Server.objects.get(id=self.kwargs['pk'])
        context = super().get_context_data(**kwargs)
        context['server'] = server
        context['heading'] = f'#{server.name}'  # h1 in server_base.html
        return context


def invite_server_user(request, pk, username):
    server = Server.objects.get(pk=pk)
    if request.user != server.owner:
        return HttpResponseForbidden()
    invited_user = User.objects.get(username=username)
    if invited_user in request.user.profile.friends.all():
        if invited_user not in server.users.all():
            invitation_id = create_random_id(10)
            invitation = ServerInvitation.objects.create(server=server, id=invitation_id, invited_user=invited_user)
            message_id = create_num_id(20)
            chat = UsersChat.objects.filter(users=request.user).filter(users=invited_user).first()
            if not chat:
                chat_id = create_num_id(10)
                while UsersChat.objects.filter(id=chat_id).first() is not None:
                    chat_id = create_num_id(10)
                chat = UsersChat.objects.create(id=chat_id)
                chat.users.add(request.user)
                chat.users.add(invited_user)
                chat.save()
            invitation_message = UsersMessage.objects.create(id=message_id,
                                                             chat=chat,
                                                             content=f'tdchat.net/i/{invitation_id}',
                                                             author=request.user)
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
        return HttpResponseRedirect(self.request.path_info)

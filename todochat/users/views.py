from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, ListView
from users.models import User, UserInvitation, UsersChat, UsersMessage
from django.shortcuts import get_object_or_404
from chat.models import Channel



def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form, 'title': 'Register'})


@login_required
def profile(request):
    username = None
    if request.user.is_authenticated:
        username = request.user.username
    return render(request, 'users/profile.html', {'title': username})


@login_required
def profile_edit(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES,  instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Profile updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'title': 'Edit profile'
    }
    return render(request, 'users/profile_edit.html', context)


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    context_object_name = "users"
    slug_field = "username"
    slug_url_kwarg = "username"
    template_name = 'users/user_detail.html'

    def post(self, request, username):
        if request.POST.get('invite_button') == 'remove':
            user = self.request.user
            removed = User.objects.filter(username=self.request.POST.get('removed')).first()
            user.profile.friends.remove(removed)
            removed.profile.friends.remove(user)
            return redirect('user_detail', request.POST.get('removed'))
        elif request.POST.get('invite_button') == 'invite':
            invited_user = User.objects.filter(username=request.POST.get('invited')).first()
            user = request.user
            if not invited_user == None:
                if UserInvitation.objects.filter(inviting=user, invited=invited_user).first() is None:
                    if UserInvitation.objects.filter(inviting=invited_user, invited=user).first():
                        invitation = UserInvitation.objects.filter(inviting=invited_user, invited=user)
                        user.profile.friends.add(invited_user)
                        invited_user.profile.friends.add(user)
                        invitation.delete()
                        return redirect('user_detail', invited_user.username)
        
                invitation = UserInvitation(inviting=user, invited=invited_user)
                invitation.save()
                return redirect('user_detail', invited_user.username)
        
        elif request.POST.get('invite_button') == 'reject':
            inviting_user = User.objects.get(username=self.request.POST.get('inviting'))
            invitation = UserInvitation.objects.get(invited=self.request.user, inviting=inviting_user)
            invitation.delete()
            return redirect('user_detail', inviting_user.username)
        
        elif request.POST.get('invite_button') == 'cancel':
            inviting_user = self.request.user
            invited_user = User.objects.get(username=self.request.POST.get('invited'))
            invitation = UserInvitation.objects.get(inviting=inviting_user, invited=invited_user)
            invitation.delete()
            return redirect('user_detail', invited_user.username)
        
        return redirect('index')


            

    def get_object(self):
        user_pk = get_object_or_404(User, username=self.kwargs.get("username"))
        return user_pk
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["taskbar_img"] = True
        friend = get_object_or_404(User, username=self.kwargs.get("username"))
        context["friend"] = friend
        context["taskbar_title"] = friend.username
        if UserInvitation.objects.filter(inviting=self.request.user, invited=friend).first() is not None:
            context["invitation"] = "waiting"
        elif UserInvitation.objects.filter(inviting=friend, invited=self.request.user).first() is not None:
            context["invitation"] = "invited"
        return context


class UserInvitations(LoginRequiredMixin, ListView):
    model = UserInvitation
    template_name = 'users/user_invitations.html'

    def post(self, request):
        user = request.user
        inviting = User.objects.filter(username=request.POST.get('inviting')).first()
        invitation = UserInvitation.objects.filter(inviting=inviting, invited=user).first()
        if request.POST.get('button') == 'accept':
            user.profile.friends.add(inviting)
            inviting.profile.friends.add(user)
            invitation.delete()
            messages.success(request, 'Added friend!')
            return redirect('user_detail', request.POST.get('inviting'))
        else:
            invitation.delete()
            return redirect('user_invitations')

    def get_queryset(self):
        return UserInvitation.objects.filter(invited=self.request.user)

class UserChatView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = UsersChat
    template_name = 'users/chat_room.html'

    def test_func(self):
        user = User.objects.get(username=self.kwargs['username'])
        if self.request.user.profile in user.friends_set.all():
            return True
        return False
       

    def get_object(self):
        friend = User.objects.get(username=self.kwargs['username'])
        chat = UsersChat.objects.filter(users=self.request.user)
        for chat_channel in chat:
            if friend in chat_channel.users.all():
                return chat_channel
        
        chat = UsersChat.objects.create(id = f'{friend.username}_{self.request.user.username}')
        chat.users.add(friend, self.request.user)
        chat.save()
        return chat
        


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["taskbar_img"] = True
        friend = User.objects.get(username=self.kwargs['username'])
        context["taskbar_title"] = friend.username
        context["friend"] = friend
        chat = UsersChat.objects.filter(users=self.request.user)
        for chat_channel in chat:
            if friend in chat_channel.users.all():
                context["messages"] = chat_channel.usersmessage_set.order_by('created')
                return context
                
        
        chat = UsersChat.objects.create(id = f'{friend.username}_{self.request.user.username}')
        chat.users.add(friend, self.request.user)
        chat.save()
        context["messages"] = chat.usersmessage_set.all()
        return context

class UserSearchView(LoginRequiredMixin, ListView):
    template_name = "user_search.html"
    model = User
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_name = self.request.GET.get('user', '')
        if not user_name == '':
            context['all_search_results'] = User.objects.filter(username__icontains=user_name )
            if context['all_search_results'].count() == 0:
                context['search_msg'] = 'Not found'
            context['prev_placeholder'] = user_name
        return context

    def post(self, request):
        prev_search = request.GET['user']
        if request.POST.get('invite_button') == 'invite':
            invited_user = User.objects.filter(username=request.POST.get('invited')).first()
            user = request.user
            if not invited_user == None:
                if UserInvitation.objects.filter(inviting=user, invited=invited_user).first() is None:
                    if UserInvitation.objects.filter(inviting=invited_user, invited=user).first():
                        invitation = UserInvitation.objects.filter(inviting=invited_user, invited=user)
                        user.profile.friends.add(invited_user)
                        invited_user.profile.friends.add(user)
                        invitation.delete()
                        return redirect(f'/search?user={prev_search}')
        
                invitation = UserInvitation(inviting=user, invited=invited_user)
                invitation.save()
                return redirect(f'/search?user={prev_search}')
        
        elif request.POST.get('invite_button') == 'reject':
            inviting_user = User.objects.get(username=self.request.POST.get('inviting'))
            invitation = UserInvitation.objects.get(invited=self.request.user, inviting=inviting_user)
            invitation.delete()
            return redirect(f'/search?user={prev_search}')
        
        elif request.POST.get('invite_button') == 'cancel':
            inviting_user = self.request.user
            invited_user = User.objects.get(username=self.request.POST.get('invited'))
            invitation = UserInvitation.objects.get(inviting=inviting_user, invited=invited_user)
            invitation.delete()
            return redirect(f'/search?user={prev_search}')
        
        return redirect('user_search')
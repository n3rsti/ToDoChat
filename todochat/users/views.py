from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import DetailView
from .models import User
from django.shortcuts import get_object_or_404


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


@method_decorator(login_required, name='dispatch')
class UserDetailView(DetailView):
    model = User
    context_object_name = "users"
    slug_field = "username"
    slug_url_kwarg = "username"
    template_name = 'users/user_detail.html'

    def get_object(self):
        user_pk = get_object_or_404(User, username=self.kwargs.get("username"))
        return user_pk

"""todochat URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from app.views import main_view, CreateServerView, DetailServerView, UpdateServerView, invite_server_user, \
    InvitationView
from users.views import register, UserInvitations, UserSearchView, invitation_card
from tasks.views import FilterTaskView, render_calendar
from django.conf import settings
from django.conf.urls.static import static
from chat.views import ChannelDetailView
from users.forms import UserLoginForm

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('', main_view, name="index"),
    path('server/<int:server_id>/tasks/', include('tasks.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html', authentication_form=UserLoginForm),
         name="login"),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name="logout"),
    path('register/', register, name="register"),
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='users/password_reset.html'), 
        name="password_reset"
        ),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='users/password_reset_done.html'), 
        name="password_reset_done"
        ),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='users/password_reset_confirm.html'), 
        name="password_reset_confirm"
        ),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='users/password_reset_complete.html'), 
        name="password_reset_complete"
        ),
    path('server/new/', CreateServerView.as_view(), name="create_server"),
    path('server/<int:pk>/details', DetailServerView.as_view(), name="server_detail"),
    path('server/<int:pk>/', DetailServerView.as_view(), name="server_detail"),
    path('server/<int:pk>/edit', UpdateServerView.as_view(), name="server_update"),
    path('server/<int:pk>/<str:room_name>/', ChannelDetailView.as_view(), name='room'),
    path('server/<int:pk>/invite/<str:username>/', invite_server_user, name='invite_server_user'),
    path('profile/invitations/', UserInvitations.as_view(), name='user_invitations'),
    path('i/<slug:pk>/', InvitationView.as_view(), name="server_invitation"),
    path('tasks/', FilterTaskView.as_view(), name="user_tasks"),
    path('profile/', include('users.urls')),
    path('search/', UserSearchView.as_view(), name="user_search"),
    path('components/invitation_card/<str:username>', invitation_card, name="invitation_card"),
    path('calendar/', render_calendar, name="render_calendar")
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

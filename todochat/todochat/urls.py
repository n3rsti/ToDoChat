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
from django.urls import path, include, re_path
from app.views import main_view, CreateServerView, DetailServerView, UpdateServerView
from users.views import register, profile, profile_edit, UserDetailView, UserInvitations, UserSearchView
from tasks.views import TaskListView, TaskDetailView, TaskUpdateView
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from chat.views import ChannelDetailView
from users.forms import UserLoginForm

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('', main_view, name="index"),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html', authentication_form=UserLoginForm), name="login"),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name="logout"),
    path('register/', register, name="register"),
    path('server/new/', CreateServerView.as_view(), name="create_server"),
    path('server/<int:pk>/details', DetailServerView.as_view(), name="server_detail"),
    path('server/<int:pk>/', DetailServerView.as_view(), name="server_detail"),
    path('server/<int:pk>/edit', UpdateServerView.as_view(), name="server_update"),
    path('server/<int:server_id>/tasks', TaskListView.as_view(), name="server_tasks"),
    path('server/<int:server_id>/tasks/<int:id>/', TaskDetailView.as_view(), name="task_detail"),
    path('server/<int:server_id>/tasks/<int:id>/edit', TaskUpdateView.as_view(), name="task_update"),
    path('profile/invitations/', UserInvitations.as_view(), name='user_invitations'),
    path('profile/', include('users.urls')),
    path('server/<int:pk>/<str:room_name>/', ChannelDetailView.as_view(), name='room'),
    path('search/', UserSearchView.as_view(), name="user_search")
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
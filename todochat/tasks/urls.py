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
from django.urls import path, include, re_path
from tasks.views import TaskListView, TaskDetailView, TaskUpdateView, change_status_view
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

urlpatterns = [
    path('', TaskListView.as_view(), name="server_tasks"),
    path('<int:id>/', TaskDetailView.as_view(), name="task_detail"),
    path('<int:id>/edit', TaskUpdateView.as_view(), name="task_update"),
    path('<int:id>/change_status', change_status_view, name="task_change_status"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
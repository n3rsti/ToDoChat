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
from django.urls import path
from users.views import profile, profile_edit, UserDetailView, UserChatView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', profile, name="profile"),
    path('edit/', profile_edit, name="profile_edit"),
    path('<str:username>/', UserDetailView.as_view(), name='user_detail'),
    path('<str:username>/chat/', UserChatView.as_view(), name='user_chat')
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

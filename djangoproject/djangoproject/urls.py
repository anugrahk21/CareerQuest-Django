"""
URL configuration for djangoproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include
from . import views
#from django.contrib.auth.views import LogoutView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('entry/', views.entry, name='entry'),
    path('view/', views.view, name='view'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    # <str:id> -> is a capture group, it will capture the id from the url and pass it to the update function
    path('update/<str:id>/', views.update, name='update'), # 'update/id/' -> url pattern for updation
    path('delete/<str:id>/', views.delete, name='delete'), # 'delete/id/' -> url pattern for deletion
    path('social-auth/', include('social_django.urls', namespace='social'))
    #or path('logout/',LogoutView.as_view(next_page='login'),name='logout')
]

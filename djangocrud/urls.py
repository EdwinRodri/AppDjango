"""djangocrud URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path
from tasks import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('tasks/', views.tareas, name='tasks'),
    path('logout/', views.salir, name='logout'),
    path('signin/', views.iniciarSesion, name='signin'),
    path('create_task/', views.create_task, name='crate_task'),
    path('detailTask/<int:task_id>', views.detailTask, name='detailTask'),
    path('detailTask/<int:task_id>/completar', views.tarea_completa, name='tarea_completa'),
    path('detailTask/<int:task_id>/eliminar', views.tarea_eliminar, name='tarea_eliminar'),
    path('tasks/completas', views.tareas_completas, name='tareas_completas'),
]

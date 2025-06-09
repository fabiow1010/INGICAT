"""
URL configuration for ingicat project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from task import views

urlpatterns = [
   path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('signup/', views.signup, name='signup'),
    path('predios/', views.predios, name='predios'),
    path('predio_completed/', views.predio_completed, name='predio_completed'),
    path('logout/', views.signout, name='logout'),
    path('signin/', views.signin, name='signin'),
    path('create_predio/', views.create_predio, name='create_predio'),
    path('predio/<int:predio_id>', views.predio_detail, name='predio_detail'),
    path('predio/<int:predio_id>/complete', views.complete_predio, name='complete_predio'),
    path('predio/<int:predio_id>/delete', views.delete_predio, name='delete_predio'),
    path('dashboard/', views.cliente_dashboard, name='cliente_dashboard'),
    path('descargar_excel/', views.descargar_excel, name='descargar_excel'),
    ]

# App/urls.py

from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('', login_required(views.home), name='home'),
    path('dashboard-admin/', views.dashboard_admin, name='dashboard_admin'),
]
# suap-clone/Calendario/urls.py
from django.urls import path
from . import views

app_name = 'Calendario'

urlpatterns = [
    path('', views.calendario_view, name='calendario'),
]
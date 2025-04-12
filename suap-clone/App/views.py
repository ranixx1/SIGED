
from django.shortcuts import render
from .models import Card
from django.contrib.auth.decorators import login_required

@login_required(login_url='/usuarios/login/')
def home(request):
   cards=Card.objects.all()
   return render(request, 'App/home.html', {'cards':cards}) 


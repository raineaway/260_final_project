from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

def index(request):
    #return HttpResponse("<html><title>To-Do List</title></html>");
    if request.user.is_authenticated():
        context = {'name': request.user.first_name}
    else:
        context = {'test': 'test'}
    return render(request, 'lists/index.html', context)

def signup(request):
    user = User.objects.create_user(request.POST['username'], request.POST['email'], request.POST['password'])
    user.first_name = request.POST['name']
    user.save()

    user = authenticate(username=request.POST['username'], password=request.POST['password'])
    login(request, user)

    #user = User.objects.get(username=request.POST['username'])

    context = {'user' : user}
    return render(request, 'lists/signup.html', context)

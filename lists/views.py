from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

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

    context = {'user' : user}
    return render(request, 'lists/signup.html', context)

def signin(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            context = {'error': 'Invalid credentials'}
            return render(request, 'lists/login.html', context)
    else:
        return render(request, 'lists/login.html')

def signout(request):
    logout(request)
    return redirect('/')

def delete_test(request):
    user = User.objects.get(username='raineaway')
    user.delete()

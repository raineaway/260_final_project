from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from lists.models import Item
from datetime import date, datetime
import json

def index(request):
    #return HttpResponse("<html><title>To-Do List</title></html>");
    if request.user.is_authenticated():
        items = Item.objects.filter(user_id=request.user.id)
        context = {'name': request.user.first_name, 'items': items, 'is_today': True, 'date':datetime.now()}
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

def create_item(request):
    if request.method == 'POST':
        if request.user.is_authenticated():
            item = Item(user=request.user, name=request.POST['task_name'])
            item.save()
        return redirect('/')
    else:
        return render(request, 'lists/create_item.html')

def check_item(request):
    if request.user.is_authenticated():
        item = Item.objects.get(id=request.POST['id'])
        if item.user_id == request.user.id:
            response = {}
            if item.status == "pending":
                item.status = "done"
                item.save()
                response = {'status':'ok'}
            else:
                item.status = "pending"
                item.save()
                response = {'status':'ok', 'item_status':'pending'}
            return HttpResponse(json.dumps(response), content_type="application/json")
        return HttpResponse(json.dumps({'status':'fail', 'message':'Invalid item.'}))
    return redirect('/')
    

def delete_test(request):
    user = User.objects.get(username='raineaway')
    
    user.delete()

    item = Item.objects.get(name='Finish the project', user=user)
    if item.count > 0:
        item.delete()


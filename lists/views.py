from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.utils import formats, timezone
from lists.models import Item
#from datetime import date, datetime
import json
import datetime
import models

def index(request):
    #return HttpResponse("<html><title>To-Do List</title></html>");
    if request.user.is_authenticated():
        if request.GET.get('date') is not None and (int(request.GET.get('date')) != 0
            and (int(request.GET.get('date')) > -8 and int(request.GET.get('date')) < 8)):

            display_date = datetime.datetime.now() + datetime.timedelta(days=int(request.GET.get('date')))
            is_today = False
            if int(request.GET.get('date') < 0):
                items = Item.objects.filter(
                    Q(user_id=request.user.id) &
                    (~Q(status='pending') &
                    Q(date_modified__range=[datetime.datetime.combine(display_date, datetime.time.min), datetime.datetime.combine(display_date, datetime.time.max)]))
                )
            else:
                items = Item.objects.filter(
                    Q(user_id=request.user.id) &
                    Q(date_modified__range=[datetime.datetime.combine(display_date, datetime.time.min), datetime.datetime.combine(display_date, datetime.time.max)])
                )
            counter = int(request.GET.get('date'))
        else:
            display_date = datetime.datetime.now()
            is_today = True
            items = Item.objects.filter(
                Q(user_id=request.user.id) &
                (Q(status='pending') |
                Q(date_modified__range=[datetime.datetime.combine(display_date, datetime.time.min), datetime.datetime.combine(display_date, datetime.time.max)]))
            )
            counter = 0
        context = {
            'name': request.user.first_name,
            'items': items,
            'is_today': is_today,
            'display_date':display_date,
            'date_counter':counter
        }
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
            item = Item(user=request.user, name=request.POST['task_name'],
                date_created=timezone.now(), date_modified=timezone.now())
                #date_created=datetime.datetime.now(), date_modified=datetime.datetime.now())
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
                item.date_modified = timezone.now()
                #item.date_modified = datetime.datetime.now()
                item.save()
                response = {'status':'ok'}
            else:
                item.status = "pending"
                item.date_modified = timezone.now()
                #item.date_modified = datetime.datetime.now()
                item.save()
                response = {'status':'ok', 'item_status':'pending'}
            return HttpResponse(json.dumps(response), content_type="application/json")
        return HttpResponse(json.dumps({'status':'fail', 'message':'Invalid item.'}))
    return redirect('/')

def cancel_item(request):
    if request.user.is_authenticated():
        item = Item.objects.get(id=request.POST['id'])
        if item.user_id == request.user.id:
            response = {}
            if item.status == "pending":
                item.status = "cancelled"
                item.date_modified = timezone.now()
                #item.date_modified = datetime.datetime.now()
                item.save()
                response = {'status':'ok'}
            else:
                response = {'status':'fail', 'message':'Invalid action.'}
            return HttpResponse(json.dumps(response), content_type="application/json")
        return HttpResponse(json.dumps({'status':'fail', 'message':'Invalid item.'}))
    return redirect('/')
    

def delete_test(request):
    user = User.objects.get(username='raineaway')
    
    user.delete()

    item = Item.objects.get(name='Finish the project', user=user)
    if item.count > 0:
        item.delete()


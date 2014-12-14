from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    #return HttpResponse("<html><title>To-Do List</title></html>");
    context = {'test': 'test'}
    return render(request, 'lists/index.html', context)

def signup(request):
    name = request.POST['name']
    context = {'name' : name}
    return render(request, 'lists/signup.html', context)

from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("<html><title>To-Do List</title></html>");


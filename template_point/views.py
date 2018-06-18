from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.template import loader
import json

@csrf_exempt
def auth_client(request):
    template = loader.get_template('auth_client.html')
    context = {}
    response = HttpResponse(template.render(context, request))
    return response

@csrf_exempt
def auth_sender(request):
    template = loader.get_template('auth_sender.html')
    context = {}
    response = HttpResponse(template.render(context, request))
    return response

@csrf_exempt
def next(request):
    template = loader.get_template('next.html')
    context = {}
    response = HttpResponse(template.render(context, request))
    return response

@csrf_exempt
def reminder_cell_is_open(request):
    template = loader.get_template('reminder_cell_is_open.html')
    context = {}
    response = HttpResponse(template.render(context, request))
    return response
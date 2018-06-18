from django.shortcuts import render
import requests
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def checked(request):
    response = {}
    response['status'] = "OK"
    return HttpResponse(json.dumps(response), content_type="application/json")

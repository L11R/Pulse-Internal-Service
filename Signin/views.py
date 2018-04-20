from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

def main_page(request):
    template = loader.get_template('Signin/index.html')
    context = {}
    response = HttpResponse(template.render(context, request))
    return response

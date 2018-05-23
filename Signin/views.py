from django.shortcuts import redirect
from django.template import loader
from django.http import HttpResponse
from datetime import datetime
from Signin import models
from django.views.decorators.csrf import csrf_exempt
from django import forms
import os
import mimetypes
from django.http import StreamingHttpResponse
from wsgiref.util import FileWrapper

PROD_URL = "https://internal.pulse.express/api/requests/from_xls/"
DEV_URL = "https://dev.internal.pulse.itcanfly.org/api/requests/from_xls/"

class SearchForm(forms.Form):
    query = forms.CharField(label='Enter a keyword to search for',
                            widget=forms.TextInput(attrs={'size': 32, 'class':'form-control search-query'}))
class FixedFileWrapper(FileWrapper):
    def __iter__(self):
        self.filelike.seek(0)
        return self

def downolad_file(request):
    the_file = '/some/file/conf.json'
    response = HttpResponse(FixedFileWrapper(open(the_file, 'rb')), content_type=mimetypes.guess_type(the_file[0]))
    response['Content-Length'] = os.path.getsize(the_file)
    response['Content-Disposition']="attachment; filename=%s" % os.path.basename(the_file)
    return response

def login_required(func):
    def login_required_handler(request):
        if not request.COOKIES.get('token'):
            return redirect('/login/')
        return func(request)
    return login_required_handler

@csrf_exempt
def login(request):
    color, msg = "grey", "Введите ваши данные ниже"
    if request.method == 'POST':
        email, password = request.POST['InputEmail'], request.POST['Inputpwd']
        c_users = models.Users.objects.filter(email=email, password=password).count()
        if c_users == 1: is_auth, user = True, models.Users.objects.get(email=email, password=password)
        else: is_auth = False
        
        if is_auth:
            info = models.Sender.objects.get(name=user.username)
            if user.stype == 1:
                response = redirect('/leroy/')
                response.set_cookie('token', info.token)
                response.set_cookie('uid', info.uid)
                response.set_cookie('URL', PROD_URL)
                response.set_cookie('type', user.stype)
                print('success cour')
                return response
            if user.stype == 0:
                response = redirect('/technical/')
                response.set_cookie('token', info.token)
                response.set_cookie('uid', info.uid)
                response.set_cookie('URL', DEV_URL)
                response.set_cookie('type', user.stype)
                print('success tech')
                return response
        else:
            color, msg = "red", 'Неверный логин/пароль'
    template = loader.get_template('Signin/login.html')
    color += "!important"
    context = {'msg': msg, "color": color}
    response = HttpResponse(template.render(context, request))
    return response

@login_required
def leroy_page(request):
    template = loader.get_template('Signin/leroy.html')
    context = {}
    response = HttpResponse(template.render(context, request))
    return response

@login_required
def techn_page(request):
    template = loader.get_template('Signin/technical.html')
    context = {}
    response = HttpResponse(template.render(context, request))
    return response

@csrf_exempt
def terminal_page(request):
    if request.POST:
        #form = SearchForm(request.POST)
        #params = dict()
        #params["search"] = form
        print(" !!!! - " ,request.body)
        the_file = 'conf.json'
        response = HttpResponse(FixedFileWrapper(open(the_file, 'rb')), content_type=mimetypes.guess_type(the_file[0]))
        response['Content-Length'] = os.path.getsize(the_file)
        response['Content-Disposition'] = "attachment; filename=%s" % os.path.basename(the_file)
        return response
    if request.GET:
        print(request.body)
    #for ee in request.GET:
    #   print("sad---" + ee + "---")
    template = loader.get_template('Signin/terminal.html')
    context = {}
    response = HttpResponse(template.render(context, request))
    return response

@login_required
def menu_page(request):
    template = loader.get_template('Signin/menu.html')
    context = {}
    response = HttpResponse(template.render(context, request))
    return response

@login_required
def cameras_page(request):
    template = loader.get_template('Signin/cameras.html')
    cameras = models.Cameras.objects.filter(stype=0)
    context = {'cameras': cameras}
    response = HttpResponse(template.render(context, request))
    return response

@login_required
def cameras_more(request):
    template = loader.get_template('Signin/cameras.html')
    cameras = models.Cameras.objects.filter(stype=1)
    context = {'cameras': cameras}
    response = HttpResponse(template.render(context, request))
    return response

def logout(request):
    response = redirect('/login/')
    response.set_cookie('token', '', expires=datetime(1970,1,1))
    return response

@login_required
def checked(request):
    api_type = int(request.COOKIES.get('type'))
    if api_type == 1:
        response = redirect('/leroy/')
        return response
    elif api_type == 0:
        response = redirect('/menu/')
        return response
    else: redirect('/login/')
from django.shortcuts import redirect
from django.template import loader
from django.http import HttpResponse
from datetime import datetime
from Signin import models

PROD_URL = "https://internal.pulse.express/api/requests/from_xls/"
DEV_URL = "https://dev.internal.pulse.itcanfly.org/api/requests/from_xls/"

def login_required(func):
    def login_required_handler(request):
        if not request.COOKIES.get('token'):
            return redirect('/login/')
        return func(request)
    return login_required_handler

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

def menu_page(request):
    template = loader.get_template('Signin/menu.html')
    context = {}
    response = HttpResponse(template.render(context, request))
    return response

def cameras_page(request):
    template = loader.get_template('Signin/cameras.html')
    context = {}
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
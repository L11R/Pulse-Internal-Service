from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from datetime import datetime

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
        if email == 'Leroy@merlin.ru' and password == '@WSX2wsx123':
            response = redirect('/leroy/')
            response.set_cookie('token', password)
            return response
        else:
            if email == 'Pulse@express.ru' and password == 'XSW@xsw2321':
                response = redirect('/technical/')
                response.set_cookie('token', password)
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


def logout(request):
    response = redirect('/login/')
    response.set_cookie('token', '', expires=datetime(1970,1,1))
    return response

@login_required
def checked(request):
    token = request.COOKIES.get('token')
    if token == '@WSX2wsx123':
        print(type(token), token)
        response = redirect('/leroy/')
        #response.set_cookie('token', password)
        return response
    if token == 'XSW@xsw2321':
        response = redirect('/technical/')
        #response.set_cookie('token', password)
        return response
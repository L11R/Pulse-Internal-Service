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
        if email != 'Leroy@merlin.ru' and password != "@WSX2wsx123":
            color, msg = "red", 'Неверный логин/пароль'
        else:
            response = redirect('/')
            response.set_cookie('token', password)
            return response
    template = loader.get_template('Signin/login.html')
    color += "!important"
    context = {'msg': msg, "color": color}
    response = HttpResponse(template.render(context, request))
    return response

@login_required
def main_page(request):
    template = loader.get_template('Signin/main.html')
    context = {}
    response = HttpResponse(template.render(context, request))
    return response

@login_required
def logout(request):
    response = redirect('/')
    response.set_cookie('token', '', expires=datetime(1970,1,1))
    return response
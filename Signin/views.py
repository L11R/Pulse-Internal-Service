from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse

def login_required(func):
    def login_required_handler(request):
        if not request.COOKIES.get('token'):
            return redirect('/login/')
        return func(request)
    return login_required_handler

def login(request):
    color, msg = "grey", "Введите ваши данные ниже"
    #color = 'grey'
    #response = HttpResponse()
    #if request.COOKIES.get('token'):
    #    return redirect('/')
    if request.method == 'POST':
        email, password = request.POST['InputEmail'], request.POST['Inputpwd']
        if email != 'Lerua@merlin.ru':
            color, msg = "red", 'Неверный логин/пароль'
        else:
            response = redirect('/')
            response.set_cookie('token', password)
            return response
    template = loader.get_template('Signin/login.html')
    color += "!important"
    context = {'msg': msg, "color": color}
    #response
    response = HttpResponse(template.render(context, request))
    #print(email, password)
    return response

@login_required
def main_page(request):
    template = loader.get_template('Signin/index.html')
    context = {}
    response = HttpResponse(template.render(context, request))
    return response
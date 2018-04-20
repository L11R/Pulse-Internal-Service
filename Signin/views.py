from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

def main_page(request):
    color, msg = 'Введите ваши данные ниже', 'grey'
    if request.method == 'POST':
        email, password = request.POST['InputEmail'], request.POST['Inputpwd']
        if email != 'Lerua@merlin.ru':
            color, msg = "red", 'Неверный логин/пароль'
        print(email, password)
    template = loader.get_template('Signin/login.html')
    color += "!important"
    context = {'msg': msg, "color": color}
    response = HttpResponse(template.render(context, request))
    return response

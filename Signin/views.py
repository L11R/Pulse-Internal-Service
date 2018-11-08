from django.shortcuts import redirect
from django.template import loader
from django.http import HttpResponse, JsonResponse
from datetime import datetime
from Signin import models
from report import models as md2
from django.views.decorators.csrf import csrf_exempt
from django import forms
from django.conf import settings
from django.core import serializers
import os
import csv
import mimetypes
#from django.http import StreamingHttpResponse
from wsgiref.util import FileWrapper
import json
#from django.template import Context, Template
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO, BytesIO
#from ho import pisa
from django.template.loader import get_template
from django.template import Context, RequestContext
#import xhtml2pdf.pisa as pisa
#import cgi
#from django.conf import settings

import requests
from django.core.files.storage import FileSystemStorage
from Signin.conf_point import *

def send_request(token, url, payload):
    HDRS = {'Content-type': 'application/json', 'Encoding': 'utf-8'}
    headers = HDRS.copy()
    headers['Authorization'] = token
    response = requests.post(url, verify=False, data=json.dumps(payload), headers=headers)
    return response

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
    response['Content-Disposition'] = "attachment; filename=%s" % os.path.basename(the_file)
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
                response.set_cookie('token', info.token, max_age=86400)
                response.set_cookie('uid', info.uid, max_age=86400)
                response.set_cookie('URL', settings.DATA['PROD_URL'] + '/requests/from_xls/', max_age=86400)
                response.set_cookie('type', user.stype, max_age=86400)
                print('success cour')
                return response
            if user.stype == 0:
                response = redirect('/technical/')
                response.set_cookie('token', info.token)
                response.set_cookie('uid', info.uid)
                response.set_cookie('URL', settings.DATA['DEV_URL'] + '/requests/from_xls/')
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

@csrf_exempt
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
def add_camera(request):
    print('sadsa')
    context = {}
    if request.method == 'POST':
        data = json.loads(request.body)
        print(data)
        context['msg'] = 'success'
    response = HttpResponse(json.dumps(context), content_type="application/json")
    return response

@csrf_exempt
@login_required
def parcels_page(request):
    if request.method == 'POST':
        print(" !!!! - ", request.body)
        response_data = {}
        
        response_data['result'] = serializers.serialize("json", md2.Report.objects.using('report').all())
        response_data['message'] = 'Some error message'
        return HttpResponse(json.dumps(response_data), content_type="application/json")
        #return JsonResponse({'foo': 'bar'})
    template = loader.get_template('Signin/table.html')
    #parcels = md2.Report.objects.using('report').filter(date_added__gte = datetime(2018,5,20))
    #context = {'parcels': parcels}
    context = {}
    response = HttpResponse(template.render(context, request))
    return response

@csrf_exempt
def get_leroy_parcels(request):
    response_data = {}
    if request.method == 'POST':
        token = request.COOKIES.get('token')
        print('POST request, token - ', token)
        from . import req_manager
        resp = req_manager.get_data(token,
                                    settings.DATA['PROD_URL'] + "/parcels/?offset = 0&limit=100&sender=Leroy%20Merlin")
        print(resp.json())
        try:
            response_data['content'] = resp.json()
            response_data['error'] = resp.text
            print('Try')
        except:
            response_data['error'] = resp.text
            print('Except')
        return HttpResponse(json.dumps(response_data), content_type="application/json")
        
@csrf_exempt
@login_required
def terminal_page(request):
    if request.POST:
        #form = SearchForm(request.POST)
        #params = dict()
        #params["search"] = form
        print(" !!!! - " ,request.body)
        the_file = 'README.md'
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

def statistic_cells(request):
    template = loader.get_template('Signin/statistic_cells.html')
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

@csrf_exempt
@login_required
def request_orders_file(request): # Should it rewrite !!
    if request.method == 'POST':
        print(request.FILES['file'].name)
        myfile = request.FILES['file']
        fs = FileSystemStorage(location=settings.REQUEST_FILES, base_url = settings.REQUEST_FILES)
        from datetime import datetime
        filename = fs.save(datetime.strftime(datetime.now(), "%Y_%m_%d-%H_%M_%S.xlsx")
, myfile)
        uploaded_file_url = fs.url(filename)
        print(filename, uploaded_file_url)
        HDRS = {'Encoding': 'utf-8'}
        headers = HDRS.copy()
        headers['Authorization'] = request.COOKIES.get('token')
        print(headers, request.COOKIES.get('uid'))
        multipart_form_data = {'file': (filename, open(uploaded_file_url, 'rb'), 'application/vnd.ms-excel')}
        try:
            resp = requests.post(
                settings.DATA['PROD_URL'] + '/requests/from_xls/',
                verify=True,
                files=multipart_form_data,
                data={"sender": request.COOKIES.get('uid')},
                headers=headers
            )
            resp_text = resp.text
            resp_status_code = resp.status_code
        except:
            resp_text, resp_status_code = 'error send request to IS', 5000
        #print(resp.text, resp.content, resp.status_code)
        resp_front = {'ERROR': True, 'RESP': resp_text, 'CODE': resp_status_code}
        if resp_status_code in (200, 201):
            resp_front['ERROR'] = False
        return HttpResponse(json.dumps(resp_front), content_type="application/json")
    return HttpResponse(json.dumps({'ERROR': True}), content_type="application/json")

@csrf_exempt
@login_required
def new_users(request):
    if request.method == 'POST':
        resp_server, response_data  = {}, {}
        print(request.FILES['file'].name)
        myfile = request.FILES['file']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        print(filename, uploaded_file_url)
        #print(request.FILES)
        data = dict.fromkeys(
            ['logistician', 'phones', 'login', 'first_name', 'middle_name', 'last_name', 'card_number', 'email',
                'blocked', 'password'])
        with open('{}/{}'.format(settings.MEDIA_ROOT,filename), encoding='cp1251') as f_obj:
            reader = csv.DictReader(f_obj, delimiter=';')
            success, errors, count, errors_login = 0, 0, 0, []
            for row in reader:
                count += 1
                if 'DPD' in row['Логин']: data['logistician'] = '81b3d261-f7e9-4a73-a080-8d7ad6bd6129'
                elif 'Leroy' in row['Логин']: data['logistician'] = 'd0e68ee2-d34f-467f-bd4f-3c399dbb5ae0'
                elif 'Pony' in row['Логин']: data['logistician'] = '906bbb10-e572-43f9-b1fc-904e484631f0'
                else: errors += 1; errors_login.append(row['Логин']); continue
                data['login'] = row['Логин']
                data['password'] = row['Пароль']
                data['phones'] = [row['Телефон']]
                data['card_number'] = row['Логин']
                data['roles'] = ['курьер']
                data['blocked'] = False
                if row['ФИО'] != '':
                    data['first_name'] = data['last_name'] = data['middle_name'] = row['ФИО']
                    if len(row['ФИО'].split()) == 3:
                        data['first_name'], data['last_name'], data['middle_name'] = row['ФИО'].split()[1][:31], row['ФИО'].split()[0][:31], row['ФИО'].split()[2][:31]
                resp = send_request(models.Sender.objects.get(name='Leroy').token, settings.DATA['PROD_URL'] + '/users/', data)
                #print(resp.json(), '!!--' ,resp.status_code)
                #print('token',models.Sender.objects.get(name='Leroy').token, 'url: ', settings.DATA['PROD_URL'] + '/couriers/', resp, data)
                if resp.status_code in [201, 200]: success += 1
                else: errors += 1; errors_login.append(row['Логин'])
                
                resp_server.update([(count, resp.json())])
                response_data['count'] = count
                response_data['errors'] = errors
                response_data['success'] = success
                response_data['error_login'] = errors_login
                response_data['resp_server'] = resp_server
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    template = loader.get_template('Signin/new_users.html')
    context = {}
    response = HttpResponse(template.render(context, request))
    return response

@csrf_exempt
@login_required
def template_views(request):
    template = loader.get_template('Signin/template_views.html')
    context = {}
    response = HttpResponse(template.render(context, request))
    return response

@csrf_exempt
@login_required
def add_apps(request):
    context = {}
    con_data = {}
    urls = []
    template = loader.get_template('Signin/add_apps.html')
    if request.method == 'POST':
        data = json.loads(request.body)
        #print(data)
        for symb in data:
            #print(symb)
            if symb['name'] == 'id' or symb['name'] == 'target_id':
                con_data[symb['name']] = symb['value'].split(', ')
            else:
                con_data[symb['name']] = symb['value']
        for id in con_data['id']:
            for target_id in con_data['target_id']:
                id.split('-')
                urls.append(con_data['host'].format(con_data['ip'], id.split('-')[0], id.split('-')[1], target_id.split('-')[1],target_id.split('-')[0]))
        print(con_data)
        #print(data[3]['value'].split(',')[0])
        context['msg'] = 'success'
        context['urls'] = urls
        response = HttpResponse(json.dumps(context), content_type="application/json")
        return response
    response = HttpResponse(template.render(context, request))
    return response
@csrf_exempt
@login_required
def checked(request):
    try:
        api_type = int(request.COOKIES.get('type'))
        if api_type == 1:
            response = redirect('/leroy/')
            return response
        elif api_type == 0:
            response = redirect('/menu/')
            return response
        else: redirect('/login/')
    except: return redirect('/leroy/')
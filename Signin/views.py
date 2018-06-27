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
#from wkhtmltopdf.views import PDFTemplateView
#from wkhtmltopdf.views import PDFTemplateResponse
#import xhtml2pdf
from xhtml2pdf import pisa
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
                response.set_cookie('token', info.token)
                response.set_cookie('uid', info.uid)
                response.set_cookie('URL', settings.DATA['PROD_URL'] + '/requests/from_xls/')
                response.set_cookie('type', user.stype)
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

def render_to_pdf(template_src, context):
    template_path = template_src
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)
    
    # create a pdf
    pisaStatus = pisa.CreatePDF(html.encode("utf-8"), dest=response, show_error_as_pdf=True, encoding='UTF-8')
    # if error then show some funy view
    if pisaStatus.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
    
    #html = template.render(context_dict)
    #result = open(filename, 'wb')  # Changed from file to filename
    #pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), result)
    #result.close()
    
    #======
    #template = get_template(template_src)
    #context = Context(context_dict)
    #html  = template.render(context_dict)
    #result = BytesIO()
    #pdf = pisa.pisaDocument(BytesIO(html.encode('utf-8')), result, show_error_as_pdf=True, encoding='UTF-8')
    #pdf = pisa.CreatePDF(BytesIO(html.encode("utf-8")), result, encoding='UTF-8', show_error_as_pdf=True)
    #response = HttpResponse(pdf, content_type='application/pdf')
    #response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'
    #return response
    #if not pdf.err:
    #    return result.getvalue()
    #return False

def render_to_pdf2(request, template_src, context_dict, name_file):
    template = get_template(template_src)
    context = {}
    ss = template.render(context, request)
    #template = loader.get_template('Signin/4.htm')
    import io
    resultFile = io.open('testirovanie.pdf', "rb")
    #pisaStatus = pisa.CreatePDF(ss, dest=resultFile)
   
    #import pdfkit
    #pdfkit.from_string(ss, 'out.pdf')
    #import pdb; pdb.set_trace()
    response = HttpResponse(resultFile.read(), content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'
    #response
    #response = HttpResponse(FixedFileWrapper(open('test.pdf', 'rb')), content_type='application/pdf')
    #resume = File.objects.get(applicant=applicant_id)
    import codecs
    #f = codecs.open('unicode.rst', encoding='utf-8')
    #resultFile = codecs.open('out.pdf', "r", encoding='ascii', errors="ignore")
    #resultFile.close()
    #resultFile.encode('utf-8')
    #response = HttpResponse(resultFile, content_type='application/pdf')
    from django.http import FileResponse
    import time
    #try:
    #except:
    #time.sleep(100)
    return response
    #return FileResponse(open('out.pdf', 'rb'), content_type='application/pdf')
    
    
    #template_srcc = 'Signin/4.htm'
    #template = get_template(template_srcc)
    #context = Context(context_dict)
    #html = template.render(context_dict)
    #result = BytesIO()
    #result = open(template_srcc, 'wb')
    #pdf = pisa.CreatePDF(BytesIO(html.encode("utf-8")), result, encoding='UTF-8', show_error_as_pdf=True)
    #pdf2 = PDFTemplateView.as_view(template_name='Signin/document2.htm', filename='my_pdf.pdf')
    #pdd = PDFTemplateView.xhtml2pdf(html)
    #responses = PDFTemplateResponse(request=request, template=template_srcc, filename="hello.pdf",
                                   #show_content_in_browser=False)
    
    #if not pdf.err:
    #    #return http.HttpResponse(result.getvalue(), mimetype='application/pdf')
    #    response = HttpResponse(result.getvalue(), content_type='application/pdf')
    #    #response = HttpResponse(responses, content_type='application/pdf')
    #    #response['Content-Disposition'] = 'attachment; filename="' + name_file + '.pdf"'
    #    return response

    #return HttpResponse(('We had some errors%s' % cgi.escape(html)))


def write_pdf(template_src, context_dict, filename):
    template = get_template(template_src)
    context = Context(context_dict)
    html  = template.render(context_dict)
    #result = open(filename, 'wb')
    result = BytesIO()# Changed from file to filename
    pdf = pisa.pisaDocument(StringIO(
        html.encode("UTF-8")), result)
    result.close()
    response = HttpResponse(pdf, content_type='application/pdf')
    #return pdf

@csrf_exempt
@login_required
def lease_page(request):
    if request.method == 'POST':
        #print(json.loads(request.body)['lastName'])
        return render_to_pdf('Signin/er2.htm', json.loads(request.body))
    import random
    rr = random.randint(1000, 9999)
    template = loader.get_template('Signin/lease.html')
    context = {'r': rr}
    response = HttpResponse(template.render(context, request))
    return response

@csrf_exempt
@login_required
def menu_lease(request):
    template = loader.get_template('Signin/menu_lease.html')
    context = {}
    response = HttpResponse(template.render(context, request))
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
@login_required
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
                data['blocked'] = False
                if row['ФИО'] != '':
                    data['first_name'] = data['last_name'] = data['middle_name'] = row['ФИО']
                    if len(row['ФИО'].split()) == 3:
                        data['first_name'], data['last_name'], data['middle_name'] = row['ФИО'].split()[1][:31], row['ФИО'].split()[0][:31], row['ФИО'].split()[2][:31]
                resp = send_request(models.Sender.objects.get(name='Leroy').token, settings.DATA['PROD_URL'] + '/couriers/', data)
                #print(resp.json(), '!!--' ,resp.status_code)
                if resp.status_code == 201: success += 1
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
def checked(request):
    api_type = int(request.COOKIES.get('type'))
    if api_type == 1:
        response = redirect('/leroy/')
        return response
    elif api_type == 0:
        response = redirect('/menu/')
        return response
    else: redirect('/login/')
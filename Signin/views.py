from django.shortcuts import redirect
from django.template import loader
from django.http import HttpResponse, JsonResponse
from datetime import datetime
from Signin import models
from report import models as md2
from django.views.decorators.csrf import csrf_exempt
from django import forms
from django.core import serializers
import os
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

PFA13 = [
    {"size_class": 2, "title": "A1", "id": "0"}, {"size_class": 1, "title": "A2", "id": "1"},
    {"size_class": 1, "title": "A3", "id": "2"}, {"size_class": 1, "title": "A4", "id": "3"},
    {"size_class": 1, "title": "A5", "id": "4"}, {"size_class": 1, "title": "A6", "id": "5"},
    {"size_class": 1, "title": "A7", "id": "6"}, {"size_class": 1, "title": "A8", "id": "7"},
    {"size_class": 1, "title": "A9", "id": "8"}, {"size_class": 2, "title": "A10", "id": "9"},
    {"size_class": 2, "title": "A11", "id": "10"}, {"size_class": 2, "title": "A12", "id": "11"}
    ]
PFA2 = [
    {"size_class":2,"title":"B1","id":"12"},{"size_class":4,"title":"B2","id":"15"}
]
PFA14 = [
    {"size_class": 2, "title": "C1", "id": "100"}, {"size_class": 1, "title": "C2", "id": "101"},
    {"size_class": 1, "title": "C3", "id": "102"}, {"size_class": 1, "title": "C4", "id": "103"},
    {"size_class": 1, "title": "C5", "id": "104"}, {"size_class": 1, "title": "C6", "id": "105"},
    {"size_class": 1, "title": "C7", "id": "106"}, {"size_class": 1, "title": "C8", "id": "107"},
    {"size_class": 1, "title": "C9", "id": "108"}, {"size_class": 1, "title": "C10", "id": "109"},
    {"size_class": 2, "title": "C11", "id": "110"}, {"size_class": 3, "title": "C12", "id": "111"}
]
PFA15 = [
    {"size_class": 2, "title": "D1", "id": "200"}, {"size_class": 1, "title": "D2", "id": "201"},
    {"size_class": 1, "title": "D3", "id": "202"}, {"size_class": 1, "title": "D4", "id": "203"},
    {"size_class": 1, "title": "D5", "id": "204"}, {"size_class": 1, "title": "D6", "id": "205"},
    {"size_class": 1, "title": "D7", "id": "206"}, {"size_class": 2, "title": "D8", "id": "207"},
    {"size_class": 3, "title": "D9", "id": "208"}, {"size_class": 3, "title": "D10", "id": "209"}
]
PFA16 = [
    {"size_class": 2, "title": "D1", "id": "200"}, {"size_class": 1, "title": "D2", "id": "201"},
    {"size_class": 1, "title": "D3", "id": "202"}, {"size_class": 1, "title": "D4", "id": "203"},
    {"size_class": 1, "title": "D5", "id": "204"}, {"size_class": 1, "title": "D6", "id": "205"},
    {"size_class": 1, "title": "D7", "id": "206"}, {"size_class": 1, "title": "D8", "id": "207"},
    {"size_class": 1, "title": "D9", "id": "208"}, {"size_class": 1, "title": "D10", "id": "209"},
    {"size_class": 1, "title": "D11", "id": "210"}, {"size_class": 4, "title": "D12", "id": "211"}
]
INFO = { "timezone": "UTC",
         "station_id": "0130",
         "cells_list": [],
         "printer": False,
         "barcode-reader-driver": "rtscan",
         "controller-driver": "engy"
         }

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
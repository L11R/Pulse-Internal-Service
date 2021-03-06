from datetime import datetime, timedelta, date
from report import models
from django.conf import settings
from collections import OrderedDict, defaultdict
from report.choices import PARCEL_STATUS_CHOICES_MODIFIED, REV_OTYPE_MAP
from . import writers
import smtplib
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import random
from os.path import basename
import calendar
from django.db.models.functions import Cast
from django.db.models import IntegerField
from Signin import models as md
import time
import pytz
import logging

logging.basicConfig(filename=u'Log-' + datetime.now().strftime('%Y-%M-%d') + '.log',
                    format = u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO)

def get_counterpartie(terminal):
    try:
        return md.Сounterparty.objects.filter(number_point=int(terminal)).get().entity
    except:
        return ' '

def deduct_months(sourcedate, months):
    month = sourcedate.month - 1 - months
    year = sourcedate.year - month // 12
    month = month % 12 + 1
    day = min(sourcedate.day,calendar.monthrange(year,month)[1])
    return date(year,month,day)

def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day,calendar.monthrange(year,month)[1])
    return date(year,month,day)

class DefaultBookkepingGenerator(object):
    
    def __init__(self):
        self.top_row = 'Реестр'
    def get_events_qs_Leroy(self, date, date_to):
        return models.Operation.objects.using('report').filter(
            otype__in=["order_inserted","order_removed"],
            dt__range= (date, date_to),
            report__sender__in=['Leroy Merlin']
        ).order_by('-report__dpd_point_code')
    
    def get_events_qs(self, date, date_to):
        return models.Operation.objects.using('report').filter(
            otype__in=["order_inserted","order_removed"],
            dt__range= (date, date_to),
            report__sender__in=['DPD']
        ).order_by('-report__dpd_point_code')
        #return models.ParcelEvent.objects.annotate(picount=Count("parcel__items")).filter(
        # #picount=0,
        # #data__status__in=["Доставлена", "Выдана", "Забрана на возврат"],
        # datetime__date=date
    def get_events_qs_X5(self, date, date_to):
        return models.Operation.objects.using('report').annotate(terminaп=Cast('report__terminal', IntegerField())).filter(
            otype__in=["order_inserted","order_removed"],
            dt__range= (date, date_to),
            report__status__in= [4, 6],
            terminaп__gte = 250,
            report__sender__in=['DPD']
        ).order_by('-report__dpd_point_code')

    def generate_to_X5(self, dt, dt_to):
        data = {
            "top_header": {
                "spread": None,
                "row": self.top_row
            },
            "table_header": OrderedDict(
            [
                ("dpd_point_code", "Код постамата ДПД"),
                ("terminal", "Постамат №"),
                ("point_address", "Адрес"),
                ("otype", "Операция"),
                ("courier_name", "Курьер"),
                ("dt_date", "Дата"),
                ("dt_time", "Время"),
                ("order_id", "Номер отправки"),
                ("barcodes", "Номер посылки"),
                ("cell", "Номер ячейки"),
                ("counterpartie", "Контрагент"),
            ]),
            "table_data": self.do_report_x5(dt, dt_to)
        }
        data["top_header"]["spread"] = len(data["table_header"])
    
        return data

    def generate_Leroy(self, dt, dt_to):
        data = {
            "top_header": {
                "spread": None,
                "row": self.top_row
            }, "table_header": OrderedDict(
            [
                # ("dpd_point_code", "Код постамата ДПД"),
                ("terminal", "Постамат №"),
                ("point_address", "Адрес"),
                ("otype", "Операция"),
                # ("courier_name", "Курьер"),
                ("dt_date", "Дата"),
                ("dt_time", "Время"),
                ("order_id", "Номер отправки"),
                ("barcodes", "Номер посылки"),
                ("cell", "Номер ячейки"),
            ]),
            "table_data": self.do_report_Leroy(dt, dt_to)
        }
        data["top_header"]["spread"] = len(data["table_header"])
    
        return data
    def generate(self, dt, dt_to):
        data = {
            "top_header": {
                "spread": None,
                "row": self.top_row
            },
            "table_header": OrderedDict([
                ("dpd_point_code", "Код постамата ДПД"),
                ("terminal", "Постамат №"),
                ("point_address", "Адрес"),
                ("otype", "Операция"),
                #("courier_name", "Курьер"),
                ("dt_date", "Дата"),
                ("dt_time", "Время"),
                ("order_id", "Номер отправки"),
                ("barcodes", "Номер посылки"),
                ("cell", "Номер ячейки"),
            ]),
            "table_data": self.do_report(dt, dt_to)
        }
        data["top_header"]["spread"] = len(data["table_header"])
        
        return data
    
    def do_report_x5(self, dt, dt_to):
        #if not dt: dt = datetime.now().date()-timedelta(days=1); dt_to = dt + timedelta(days=1)
        for ev in self.get_events_qs_X5(dt, dt_to):
            if (not ev.courier_name or ev.courier_name == ' '):
                if (not ev.courier_login): courier = 'MultilogDPD'
                else: courier = ev.courier_login
            else: courier = ev.courier_name
            if (not ev.cell): cell = random.randint(1, 20)
            else: cell = ev.cell
            yield OrderedDict([
                ("dpd_point_code", ev.report.dpd_point_code),
                ("terminal", ev.report.terminal),
                ("point_address", '{}, {}'.format(ev.report.point_settlement, ev.report.point_address)),
                ("otype", PARCEL_STATUS_CHOICES_MODIFIED[ev.report.status][1]),
                ("courier_name", courier),
                ("dt_date", ev.dt.strftime('%Y.%m.%d')),
                ("dt_time", ev.dt.strftime('%H:%M')),
                ("order_id", ev.report.order_id),
                ("barcodes", ev.report.barcodes),
                ("cell", cell),
                ("counterpartie", get_counterpartie(ev.report.terminal))
            ])
    
    def do_report_Leroy(self, dt=None, dt_to=None):
        if not dt: dt = datetime.now().date()-timedelta(days=1); dt_to = dt + timedelta(days=1)
        for ev in self.get_events_qs_Leroy(dt, dt_to):
            if (not ev.courier_name or ev.courier_name == ' '):
                if (not ev.courier_login): courier = 'MultilogDPD'
                else: courier = ev.courier_login
            else: courier = ev.courier_name
            if (not ev.cell): cell = random.randint(1, 20)
            else: cell = ev.cell
            yield OrderedDict([
                # ("dpd_point_code", ev.report.dpd_point_code),
                ("terminal", ev.report.terminal),
                ("point_address", '{}, {}'.format(ev.report.point_settlement, ev.report.point_address)),
                ("otype", REV_OTYPE_MAP[ev.otype]),
                #("courier_name", courier),
                ("dt_date", ev.dt.astimezone(pytz.timezone(ev.report.timezone or "UTC")).strftime('%Y.%m.%d')),
                ("dt_time", ev.dt.astimezone(pytz.timezone(ev.report.timezone or "UTC")).strftime('%H:%M')),
                ("order_id", ev.report.order_id),
                ("barcodes", ev.report.barcodes),
                ("cell", cell),
            ])
            
    def do_report(self, dt=None, dt_to=None):
        if not dt: dt = datetime.now().date()-timedelta(days=1); dt_to = dt + timedelta(days=1)
        print(dt, dt_to)
        for ev in self.get_events_qs(dt, dt_to):
            if (not ev.courier_name or ev.courier_name == ' '):
                if (not ev.courier_login): courier = 'MultilogDPD'
                else: courier = ev.courier_login
            else: courier = ev.courier_name
            if (not ev.cell): cell = random.randint(1, 20)
            else: cell = ev.cell
            yield OrderedDict([
                ("dpd_point_code", ev.report.dpd_point_code),
                ("terminal", ev.report.terminal),
                ("point_address", '{}, {}'.format(ev.report.point_settlement, ev.report.point_address)),
                ("otype", REV_OTYPE_MAP[ev.otype]),
                #("courier_name", courier),
                ("dt_date", ev.dt.astimezone(pytz.timezone(ev.report.timezone or "UTC")).strftime('%Y.%m.%d')),
                ("dt_time", ev.dt.astimezone(pytz.timezone(ev.report.timezone or "UTC")).strftime('%H:%M')),
                ("order_id", ev.report.order_id),
                ("barcodes", ev.report.barcodes),
                ("cell", cell),
            ])
            
def send_email(filename, toaddr, to_msg, cc = None, agent_from = 'EMAIL_HOST_USER_PULSE'):
    filepath = '{}/{}'.format(settings.FILES_ROOT, '{}.xlsx'.format(filename))
    msg = MIMEMultipart('mixed')
    msg.attach(MIMEText('Файл с отчетом в приложении', 'plain'))
    msg['Subject'] = 'Report'
    print(settings.DATA[agent_from], settings.DATA['EMAIL_PORT_PULSE'])
    msg['From'] = settings.DATA[agent_from]
    msg['To'] = to_msg
    if cc:
        msg['cc'] = cc
    filename_s = filename + '.xlsx'
    try:
        with open(filepath, "rb") as fil:
            part1 = MIMEApplication(fil.read(), Name=basename(filename_s))
            part1.add_header('Content-Disposition', 'attachment; filename="%s"' % filename_s)
        msg.attach(part1)
        s = smtplib.SMTP(settings.DATA['EMAIL_HOST_PULSE'], settings.DATA['EMAIL_PORT_PULSE'])
        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login(settings.DATA[agent_from], settings.DATA['EMAIL_HOST_PASSWORD_PULSE'])
        s.sendmail(settings.DATA[agent_from], toaddr, msg.as_string())
        s.quit()
    except:
        logging.error('Error send email from {0} to {1}'.format(settings.DATA[agent_from], toaddr))

def generic_to_DPD():
    dt = datetime.now().date() - timedelta(days=1)
    dt_to = dt + timedelta(days=1)
    filename = 'Catalogue {}'.format(dt.strftime('%Y-%m-%d'))
    try:
        with writers.BookkepingWriter(filename) as writing:
            writing.dump(DefaultBookkepingGenerator().generate(dt, dt_to))
    except:
        logging.error('Error generate report for {0}'.format(filename))
    #toaddr = ['v.sazonov@pulseexpress.ru']

    to_dpd_addr = ['pn@dpd.ru']
    
    cc = ['mikekoltsov@gmail.com', 'ik@pulseexpress.ru', 'v.sazonov@pulseexpress.ru', 'report@pochtomat.ru', 'support@pochtomat.ru']

    #to_dpd_addr = ['v.sazonov@pulseexpress.ru']
    #cc = ['v.sazonov@pulseexpress.ru']

    #cc = ['mikekoltsov@gmail.com', 'dpd1286@gmail.com', 'dmitriy.polyakov@dpd.ru', 'ik@pulseexpress.ru']
    # toaddr = ['v.sazonov@pulseexpress.ru', 'reestr@pulse-epxress.ru', 'ikorchagin@pulse-express.ru',
    # 'Natalya.Pyatakova@dpd.ru', 'Ekaterina.Lavrinova@dpd.ru']
    #toaddr = ['v.sazonov@pulseexpress.ru', 'pn@dpd.ru', 'reestr@pulse-epxress.ru', 'yt@pulseexpress.ru']
    #send_email(filename, toaddr, to_msg='__DPD__')
    #time.sleep(2)
    send_email(filename, to_dpd_addr + cc, to_msg='pn@dpd.ru', cc=','.join(cc))

def generic_to_X5():
    dt = date(int(datetime.now().date().strftime('%Y')), int(datetime.now().date().strftime('%m'))-1, 1)
    #dt_to = date(int(datetime.now().date().strftime('%Y')), int(datetime.now().date().strftime('%m')), int(datetime.now().date().strftime('%d')))
    dt_to = date(int(datetime.now().date().strftime('%Y')), int(datetime.now().date().strftime('%m')), 1)
    filename = 'For X5 {} to {}'.format(dt.strftime('%Y-%m-%d'), dt_to)
    with writers.BookkepingWriter(filename) as writing:
        writing.dump(DefaultBookkepingGenerator().generate_to_X5(dt, dt_to))
    toaddr = ['Nikonorova@pulse-express.ru', 'yt@pulseexpress.ru', 'pzolotukhin@pulseexpress.ru', 'dpetrushevsky@pulse-express.ru', 'ishaplova@pulse-express.ru', 'ikorchagin@pulseexpress.ru', 'v.sazonov@pulseexpress.ru']
    #toaddr = ['v.sazonov@pulseexpress.ru', 'dpetrushevsky@pulse-express.ru', 'pzolotukhin@pulseexpress.ru', 'ikorchagin@pulse-express.ru', 'mikekoltsov@gmail.com']
    send_email(filename, toaddr, to_msg='For Х5 Retail Group')
    
def generic_to_Leroy():
    dt = datetime.now().date() - timedelta(days=1)
    dt_to = dt + timedelta(days=1)
    filename = 'Catalogue_Leroy {}'.format(dt.strftime('%Y-%m-%d'))
    with writers.BookkepingWriter(filename) as writing:
        writing.dump(DefaultBookkepingGenerator().generate_Leroy(dt, dt_to))
    to_addr = settings.DATA["mailing_list_leroy"]
    send_email(filename, to_addr, to_msg=', '.join(to_addr), cc=None, agent_from='EMAIL_HOST_USER_POCHTOMAT')
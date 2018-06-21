from openpyxl import Workbook
from openpyxl.styles import PatternFill, Border, Side, Alignment, Protection, Font, Side
from django.conf import settings
from datetime import datetime, timedelta
from report import models
from django.conf import settings
from collections import OrderedDict, defaultdict
from report.choices import PARCEL_STATUS_CHOICES
from . import writers

import smtplib
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart

class DefaultBookkepingGenerator(object):
    
    def __init__(self):
        self.top_row = 'Реестр'
    
    def get_events_qs(self, date):
        return models.Operation.objects.using('report').filter(dt__gte = date)
        #return models.ParcelEvent.objects.annotate(picount=Count("parcel__items")).filter(
        # #picount=0,
        # #data__status__in=["Доставлена", "Выдана", "Забрана на возврат"],
        # datetime__date=date
    
    def generate(self):
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
                ("courier_name", "Курьер"),
                ("dt_date", "Дата"),
                ("dt_time", "Время"),
                ("order_id", "Номер отправки"),
                ("barcodes", "Номер посылки"),
                #("cell", "Номер ячейки"),
            ]),
            "table_data": self.do_report()
        }
        data["top_header"]["spread"] = len(data["table_header"])
        
        return data
        
    def do_report(self, dt=datetime.now().date()-timedelta(days=1)):
        for ev in self.get_events_qs(dt):
            if int(ev.report.terminal) in range(201, 251):
                yield OrderedDict([
                    ("dpd_point_code", ev.report.dpd_point_code),
                    ("terminal", ev.report.terminal),
                    ("point_address", '{}, {}'.format(ev.report.point_settlement, ev.report.point_address)),
                    ("otype", PARCEL_STATUS_CHOICES[ev.report.status][1]),
                    ("courier_name", ev.courier_login),
                    ("dt_date", ev.dt.strftime('%Y.%m.%d')),
                    ("dt_time", ev.dt.strftime('%H:%M')),
                    ("order_id", ev.report.order_id),
                    ("barcodes", ev.report.barcodes),
                    #("cell", "Номер ячейки"),
                ])

def generic():
    filename = 'report'
    with writers.BookkepingWriter(filename) as writing:
        writing.dump(DefaultBookkepingGenerator().generate())

    
    filepath = '{}/{}'.format(settings.FILES_ROOT, '{}.xlsx'.format(filename))
    toaddr = ['v.sazonov@pulseexpress.ru', 'mikekoltsov@gmail.com']
    msg = MIMEMultipart('mixed')
    msg['Subject'] = 'Report'
    print(settings.DATA['EMAIL_HOST_USER_PULSE'], settings.DATA['EMAIL_PORT_PULSE'])
    msg['From'] = settings.DATA['EMAIL_HOST_USER_PULSE']
    msg['To'] = '__PULSE__'
    msg['cc'] = '__PULSE-EXPRESS__'
    try:
        fo = open(filepath, 'rb')
        filecontent = fo.read()
        fo.close()
        part1 = MIMEApplication(filecontent, 'application/xls;name=report.xlsx')
    except:
        part1 = MIMEText('\nError creating report file', 'plain')

    text_info = '\nСтатистика ->> \n'
    part2 = MIMEText(text_info, 'plain')
    msg.attach(part1)
    msg.attach(part2)
    s = smtplib.SMTP(settings.DATA['EMAIL_HOST_PULSE'], settings.DATA['EMAIL_PORT_PULSE'])
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(settings.DATA['EMAIL_HOST_USER_PULSE'], settings.DATA['EMAIL_HOST_PASSWORD_PULSE'])
    s.sendmail(settings.DATA['EMAIL_HOST_USER_PULSE'], toaddr, msg.as_string())
    s.quit()
    #writers.BookkepingWriter('report').dump()
    #wb = Workbook()
    #ws = wb.active
    #ws.title = 'consignors'
    #ws.append(list(DefaultBookkepingGenerator('New').generate()))
    #wb.save('{}/{}'.format(settings.FILES_ROOT,'{}.xlsx'.format(filename)))
    #print('MAIN.XLS')
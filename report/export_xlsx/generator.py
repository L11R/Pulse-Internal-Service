from openpyxl import Workbook
from openpyxl.styles import PatternFill, Border, Side, Alignment, Protection, Font, Side
from django.conf import settings
from datetime import datetime, timedelta
from report import models
from django.conf import settings
from collections import OrderedDict, defaultdict
from report.choices import PARCEL_STATUS_CHOICES
from . import writers

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
                    ("otype", PARCEL_STATUS_CHOICES[ev.report.status]),
                    ("courier_name", ev.courier_login),
                    ("dt_date", ev.dt.strftime('%Y.%m.%d')),
                    ("dt_time", ev.dt.strftime('%H:%M')),
                    ("order_id", ev.report.order_id),
                    ("barcodes", ', '.join(ev.report.barcodes)),
                    #("cell", "Номер ячейки"),
                ])

def generic():
    writers.BookkepingWriter('report').dump(DefaultBookkepingGenerator().generate())
    #wb = Workbook()
    #ws = wb.active
    #ws.title = 'consignors'
    #ws.append(list(DefaultBookkepingGenerator('New').generate()))
    #wb.save('{}/{}'.format(settings.FILES_ROOT,'{}.xlsx'.format(filename)))
    #print('MAIN.XLS')
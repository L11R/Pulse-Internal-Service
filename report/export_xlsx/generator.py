from openpyxl import Workbook
from openpyxl.styles import PatternFill, Border, Side, Alignment, Protection, Font, Side
from django.conf import settings
from collections import OrderedDict, defaultdict
from datetime import datetime, timedelta
from pulse_apps.core import models
from django.db.models import Count

class Defffa():
    
    def __init__(self):
        self.top_row = 'Реестр'

    def get_events_qs(self, date):
        return models.ParcelEvent.objects.annotate(picount=Count("parcel__items")).filter(
        picount=0,
        data__status__in=["Доставлена", "Выдана", "Забрана на возврат"],
        datetime__date=date
    )

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
        
    def do_report(self, dt=datetime(2018, 6, 10)):
        while dt.date() <= datetime.now().date():
            dt += timedelta(days=1)
            for ev in self.get_events_qs(dt):
                if int(ev.parcel.point.parcelterminal.number) in range(201, 251):
                    yield OrderedDict([
                        ("dpd_point_code", ev.parcel.point.parcelterminal.dpd_point_code),
                        ("terminal", ev.parcel.point.parcelterminal.number),
                        ("point_address", '{}, {}'.format(ev.parcel.point.settlement, ev.parcel.point.address)),
                        ("otype", ev.data['status']),
                        #("courier_name", "Курьер"),
                        ("dt_date", ev.datetime.strftime('%Y.%m.%d')),
                        ("dt_time", ev.datetime.strftime('%H:%M')),
                        ("order_id", ev.parcel.order_id),
                        ("barcodes", ', '.join(ev.parcel.barcodes)),
                        #("cell", "Номер ячейки"),
                    ])

def generic(filename):
    wb = Workbook()
    ws = wb.active
    ws.title = 'consignors'
    ws.append(list(DefaultBookkepingGenerator('New').generate()))
    wb.save('{}/{}'.format(settings.FILES_ROOT,'{}.xlsx'.format(filename)))
    print('MAIN.XLS')
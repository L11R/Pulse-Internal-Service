from openpyxl import Workbook
from openpyxl.styles import PatternFill, Border, Side, Alignment, Protection, Font, Side
from django.conf import settings
from collections import OrderedDict, defaultdict


class DefaultBookkepingGenerator(object):
    
    def __init__(self, name):
        self.top_row = name
    
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
                ("cell", "Номер ячейки"),
            ]),
            "table_data": self.do_report()
        }
        data["top_header"]["spread"] = len(data["table_header"])
        
        return data["table_header"].values()
        
    def do_report(self):
        pass

def generic(filename):
    wb = Workbook()
    ws = wb.active
    ws.title = 'consignors'
    ws.append(list(DefaultBookkepingGenerator('New').generate()))
    wb.save('{}/{}'.format(settings.FILES_ROOT,'{}.xlsx'.format(filename)))
    print('MAIN.XLS')
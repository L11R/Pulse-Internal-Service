# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from report.export_xlsx import generator



OTYPE_MAP = {
    "Доставлена": "order_inserted",
    "Выдана": "receive_result",
    "Забрана на возврат": "order_removed"
}

class Command(BaseCommand):
    help = 'Creates and sends report on consignors from Information System'
    
    def handle(self, *args, **options):
        generator.generic_to_DPD()
        #generator.generic()



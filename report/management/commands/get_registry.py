# -*- coding: utf-8 -*-

from django.conf import settings
from django.core.management.base import BaseCommand
from datetime import datetime, timedelta
from pulse_apps.core import models
from django.db.models import Count
from report import models as md_report
from decimal import Decimal
import uuid


OTYPE_MAP = {
    "Доставлена": "order_inserted",
    "Выдана": "receive_result",
    "Забрана на возврат": "order_removed"
}



class Command(BaseCommand):
    help = 'Creates and sends report on consignors from Information System'

    def handle(self, *args, **options):
        print('Start command')
        #dt = datetime.now().date()-timedelta(days=1)
        #creation_of_departure(get_events_qs(dt))


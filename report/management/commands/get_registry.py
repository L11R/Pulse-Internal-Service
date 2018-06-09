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


def get_events_qs(date):
    return models.ParcelEvent.objects.annotate(picount=Count("parcel__items")).filter(
        picount=0,
        data__status='В доставке',
        datetime__date=date
    )


def get_events_qs_full(date):
    return models.ParcelEvent.objects.annotate(picount=Count("parcel__items")).filter(
        picount=0,
        data__status='В доставке',
        datetime__date__gte=date
    )


def create_operation(report, event):
    op = md_report.Operation(
        idd=event.uid,
        report=report,
        dt=event.datetime,
    )
    if event.parcel.cell:
        op.cell = event.parcel.cell.number

    return op


def load_operations(report, ev):
    if ev.data['status'] not in ["Доставлена", "Выдана", "Забрана на возврат"]:
        return

    op = create_operation(report, ev)

    op.otype = OTYPE_MAP[ev.data['status']]
    pp = ev.parcel
    if op.otype == 'order_inserted':
        if pp.courier:
            op.courier_name = pp.courier.name
            op.courier_login = pp.courier.login
    elif op.otype == 'order_removed':
        pass
        # We should have parcel.courier_takeout
        # if pp.courier_takeout:
        #     op.courier_name = pp.courier.name
        #     op.courier_login = pp.courier.login

    op.save(using='report')


def creation_of_departure(events):
    for ev in events:
        pp = ev.parcel
        record_field = md_report.Report()
        record_field.idd = pp.uid
        record_field.order_id = pp.order_id
        record_field.barcodes = ','.join(pp.barcodes)
        record_field.terminal = pp.point.parcelterminal.number
        record_field.dpd_point_code = pp.point.parcelterminal.dpd_point_code
        record_field.point_settlement = pp.point.settlement
        record_field.point_address = pp.point.address
        record_field.consignor = pp.consignor
        record_field.date_added = datetime.combine(datetime.date(pp.date_added), datetime.time(pp.date_added))
        record_field.status = pp.status
        record_field.cod = pp.cod
        record_field.partner_service_fee = pp.partner_service_fee
        record_field.declared_price = pp.declared_price
        record_field.phone = pp.receiver.phone.as_e164
        record_field.sender = str(pp.sender)
        record_field.save(using='report')
        load_operations(record_field, ev)


def create_all(dt=datetime(2018, 1, 1)):
    return creation_of_departure(get_events_qs_full(dt))


class Command(BaseCommand):
    help = 'Creates and sends report on consignors from Information System'

    def handle(self, *args, **options):
        print('Start command')
        #dt = datetime.now().date()-timedelta(days=1)
        #creation_of_departure(get_events_qs(dt))


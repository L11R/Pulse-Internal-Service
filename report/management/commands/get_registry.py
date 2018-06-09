# -*- coding: utf-8 -*-


from django.core.management.base import BaseCommand



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


# -*- coding: utf-8 -*-

from datetime import datetime

from django.core.management.base import BaseCommand
import datetime
from datetime import timedelta
from sms import models

def params(dt, msg_status):
    return {'date_modified__range': (dt, dt + timedelta(days=1)),
             'msg_status': msg_status}


class Command(BaseCommand):
    help = 'Create report for sms statics'
    
    def handle(self, *args, **options):
        dt = datetime.datetime.now().date()
        for i in range(5):
            try:
                st = models.Statistics_msg.objects.using('report').filter(date=dt).get()
            except:
                st = models.Statistics_msg()
                st.date = dt
            st.new_msg = models.Sms.objects.using('report').filter(**params(dt, 0)).count()
            st.sent_msg = models.Sms.objects.using('report').filter(**params(dt, 1)).count()
            st.planned_msg = models.Sms.objects.using('report').filter(**params(dt, 2)).count()
            st.no_sent_msg = models.Sms.objects.using('report').filter(**params(dt, 3)).count()
            st.techn_problem = models.Sms.objects.using('report').filter(**params(dt, 4)).count()
            st.save(using='report')
            dt -= timedelta(days=1)

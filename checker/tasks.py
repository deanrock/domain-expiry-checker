from __future__ import absolute_import

from datetime import datetime

from celery import shared_task
import whois as whois_lib
import json
from checker.models import Domain
import decimal
from django.db.models.base import ModelState

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
       if hasattr(obj, 'isoformat'):
           return obj.isoformat()
       elif isinstance(obj, decimal.Decimal):
           return float(obj)
       elif isinstance(obj, ModelState):
           return None
       else:
           return json.JSONEncoder.default(self, obj)

@shared_task
def whois(id):
    domain = Domain.objects.get(id=id)

    result = None
    try:
        result = whois_lib.whois(domain.name)
    except:
        pass

    if not result:
        domain.status = 'check-failed'

    if result:
        domain.response = json.dumps(result.__dict__, cls=DateTimeEncoder)
        if result.expiration_date: domain.expiration_date = result.expiration_date[-1]
        domain.registrar = result.registrar
        if result.creation_date: domain.creation_date = result.creation_date[-1]
        if result.updated_date: domain.last_updated = result.updated_date[-1]

        if domain.expiration_date:
            if domain.expiration_date < datetime.now():
                domain.status = 'expired'
            else:
                domain.status = 'good'
        else:
            domain.status = 'check-failed'

    domain.last_checked = datetime.now()
    domain.save()

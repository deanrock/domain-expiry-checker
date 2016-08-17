from datetime import datetime

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from checker.models import Source
from .models import Domain
from .tasks import whois


@csrf_exempt
def import_newlines(request):
    # find source
    if not 'HTTP_AUTH_KEY' in request.META:
        return HttpResponse('Unauthorized', status=401)

    source = Source.objects.filter(auth_key=request.META['HTTP_AUTH_KEY']).first()

    if not source:
        return HttpResponse('Unauthorized', status=401)

    content = request.body.decode('utf-8')
    lines = content.split('\n')

    for line in lines:
        if len(line) > 0:
            domain = Domain.objects.filter(name=line).first()

            if not domain:
                domain = Domain()
                domain.name = line
                domain.last_seen = datetime.now()
                domain.save()

            if not source in domain.sources.all():
                domain.sources.add(source)

            domain.last_seen = datetime.now()
            domain.save()
            whois.delay(domain.id)

    return HttpResponse('OK')

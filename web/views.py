from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from web.models import Resource
from django.shortcuts import redirect
from web.utils import is_due_for_review
from operator import attrgetter
import datetime
import logging
from django.contrib.auth.decorators import login_required

logger = logging.getLogger(__name__)

logging.basicConfig(
    level = logging.INFO,
    format = " %(levelname)s %(name)s: %(message)s",
)

@login_required
def index(request):
    today = datetime.date.today()

    to_review = [res for res in Resource.objects.all() if is_due_for_review(res.rep_count, res.last_rep_date, today)]

    return render(request, 'web/index.html', {'resources': sorted(to_review, key=attrgetter('last_rep_date'))})

@login_required
def add_new_resource(request):
    today = datetime.date.today()
    caption = request.POST['caption']
    location = request.POST['location']

    if not caption or not location:
        return HttpResponse(status=400, reason='caption or location is empty')

    Resource.objects.create(caption=caption, location=location, notes=request.POST['notes'], last_rep_date=today)
    return HttpResponse()

@login_required
def reviewed(request):
    new_rep_count = int(request.POST['new_rep_count'])
    if new_rep_count < 0:
        logger.warning('Attempt to set rep count to: ' + new_rep_count)

    res_id = int(request.POST['resource_id'])
    res = Resource.objects.filter(id=res_id)
    if res.count() == 0:
        logger.warning('Attempt to set rep count to non existent ID: ' + res_id)

    for r in res:
        logger.info('Reviewed resource ' + str(res_id) +
                    '; old rep_count: ' + str(r.rep_count) +
                    '; new rep_count: ' + str(new_rep_count))
        r.rep_count = new_rep_count
        r.last_rep_date = datetime.date.today()
        r.save()

    return HttpResponse()
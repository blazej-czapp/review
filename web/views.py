from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from web.models import Resource
from django.shortcuts import redirect
from operator import attrgetter
import datetime
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from supermemo2 import SMTwo

@login_required
@require_http_methods(["GET"])
def index(request):
    # arbitrary ordering just to keep the list stable
    return render(request, 'web/index.html')

@login_required
@require_http_methods(["GET"])
def review_list(request):
    to_review = Resource.objects.filter(next_review__lte=datetime.date.today(), added_by=request.user)

    # arbitrary ordering just to keep the list stable
    return render(request, 'web/review_list.html', {'resources': sorted(to_review, key=attrgetter('id'))})

@login_required
@require_http_methods(["POST"])
def add_new_resource(request):
    today = datetime.date.today()
    caption = request.POST['caption']

    if not caption:
        return HttpResponse(status=400, reason='caption is empty')

    # arbitrarily setting initial quality to 3 (that's what they do in supermemo2 docs)
    sm = SMTwo(quality=3, first_visit=True)

    Resource.objects.create(added_by=request.user, caption=caption, location=request.POST['location'],
                            notes=request.POST['notes'], interval=sm.new_interval, repetitions=sm.new_repetitions,
                            next_review=sm.next_review, easiness=sm.new_easiness)
    return HttpResponse()

@login_required
@require_http_methods(["POST"])
def reviewed(request):
    quality = int(request.POST['quality'])
    if quality < 0 or quality > 5:
        return HttpResponse(status=400, reason='Invalid recall quality: ' + quality)

    res_id = int(request.POST['resource_id'])
    res = Resource.objects.filter(id=res_id)
    if res.count() == 0:
        return HttpResponse(status=400, reason='Attempt to review a non existent ID: ' + res_id)

    for r in res:
        # Take current review's quality and infer new values for review variables:
        #  - repetitions: quality <3 breaks the streak and resets it to 1, I think
        #  - easiness is lowered if quality is low
        #  - interval is shortened if quality is low
        sm = SMTwo(quality=quality, interval=r.interval,
                   repetitions=r.repetitions, easiness=r.easiness)

        today = datetime.date.today()

        r.interval = sm.new_interval
        r.repetitions = sm.new_repetitions
        r.easiness = sm.new_easiness
        r.next_review = today + datetime.timedelta(days=sm.new_interval)
        r.save()

    return HttpResponse()

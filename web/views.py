import datetime
import json

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from web.models import Resource
from django.shortcuts import redirect
from operator import attrgetter
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from web.utils import is_hyperlink
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
@require_http_methods(["GET"])
def get_raw_resource_data(request):
    res = Resource.objects.filter(added_by=request.user, id=request.GET['resource_id'])
    assert res.count() == 1
    for r in res:
        data = { "caption": r.caption, "location": r.location, "notes": r.notes }
        return HttpResponse(json.dumps(data), content_type="application/json")

@login_required
@require_http_methods(["POST"])
def add_new_resource(request):
    today = datetime.date.today()
    caption = request.POST['caption']

    if not caption:
        return HttpResponse(status=400, reason='caption is empty')

    # arbitrarily setting initial quality to 3 (that's what they do in supermemo2 docs)
    sm = SMTwo(quality=3, first_visit=True)

    # checking is_hyperlink synchronously because it's easier
    Resource.objects.create(added_by=request.user, caption=caption, location=request.POST['location'],
                            is_hyperlink=is_hyperlink(request.POST['location']),
                            notes=request.POST['notes'], interval=sm.new_interval, repetitions=sm.new_repetitions,
                            next_review=sm.next_review, easiness=sm.new_easiness)
    return HttpResponse()

@login_required
@require_http_methods(["POST"])
def edit_existing_resource(request):
    caption = request.POST['caption']

    if not caption:
        return HttpResponse(status=400, reason=f'caption is empty')

    res_id = request.POST['resource_id']
    res = Resource.objects.filter(added_by=request.user, id=res_id)
    if res.count() == 0:
        # report 400 even if res exists but is owned by a different user, there's no need to leak that information
        return HttpResponse(status=400, reason='Attempt to edit a non existent ID: ' + res_id)

    assert res.count() == 1
    for r in res:
        # If location hasn't changed, preserve the original value of is_hyperlink - if something was a live hyperlink
        # at creation then it is still a hyperlink now (but perhaps one gone bad).
        if r.location != request.POST['location']:
            r.is_hyperlink = is_hyperlink(request.POST['location'])
        r.caption = caption
        r.location = request.POST['location']
        r.notes = request.POST['notes']
        r.save()

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

    assert res.count() == 1
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

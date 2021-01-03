import datetime
import json

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from web.models import ReviewItem
from django.shortcuts import redirect
from operator import attrgetter
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from web.utils import conversion_to_hyperlink
from supermemo2 import SMTwo

@login_required
@require_http_methods(["GET"])
def index(request):
    # arbitrary ordering just to keep the list stable
    return render(request, 'web/index.html')

@login_required
@require_http_methods(["GET"])
def review_list(request):
    to_review = ReviewItem.objects.filter(next_review__lte=datetime.date.today(), added_by=request.user)

    # arbitrary ordering just to keep the list stable
    return render(request, 'web/review_list.html', {'review_items': sorted(to_review, key=attrgetter('id'))})

@login_required
@require_http_methods(["GET"])
def get_raw_review_item_data(request):
    items = ReviewItem.objects.filter(added_by=request.user, id=request.GET['review_item_id'])
    assert items.count() == 1
    for item in items:
        data = { "caption": item.caption, "location": item.location, "notes": item.notes }
        return HttpResponse(json.dumps(data), content_type="application/json")

@login_required
@require_http_methods(["POST"])
def add_new_review_item(request):
    today = datetime.date.today()
    caption = request.POST['caption']

    if not caption:
        return HttpResponse(status=400, reason='caption is empty')

    # arbitrarily setting initial quality to 3 (that's what they do in supermemo2 docs)
    sm = SMTwo(quality=3, first_visit=True)

    conv = conversion_to_hyperlink(request.POST['location'])
    sanitized_location = conv + request.POST['location'] if conv is not None else request.POST['location']
    ReviewItem.objects.create(added_by=request.user, caption=caption, location=sanitized_location,
                            is_hyperlink=conv is not None, notes=request.POST['notes'], interval=sm.new_interval,
                            repetitions=sm.new_repetitions, next_review=sm.next_review, easiness=sm.new_easiness)
    return HttpResponse()

@login_required
@require_http_methods(["POST"])
def edit_existing_review_item(request):
    caption = request.POST['caption']

    if not caption:
        return HttpResponse(status=400, reason=f'caption is empty')

    item_id = request.POST['review_item_id']
    items = ReviewItem.objects.filter(added_by=request.user, id=item_id)
    if items.count() == 0:
        # report 400 even if item exists but is owned by a different user, there's no need to leak that information
        return HttpResponse(status=400, reason='Attempt to edit a non existent ID: ' + item_id)

    assert items.count() == 1
    for item in items:
        # If location hasn't changed, preserve the original value of is_hyperlink - if something was a live hyperlink
        # at creation then it is still a hyperlink now (but perhaps one gone bad).
        if item.location != request.POST['location']:
            conv = conversion_to_hyperlink(request.POST['location'])
            sanitized_location = conv + request.POST['location'] if conv is not None else request.POST['location']
            item.is_hyperlink = conv is not None
            item.location = sanitized_location
        item.caption = caption
        item.location = request.POST['location']
        item.notes = request.POST['notes']
        item.save()

    return HttpResponse()

@login_required
@require_http_methods(["POST"])
def reviewed(request):
    quality = int(request.POST['quality'])
    if quality < 0 or quality > 5:
        return HttpResponse(status=400, reason='Invalid recall quality: ' + quality)

    item_id = int(request.POST['review_item_id'])
    items = ReviewItem.objects.filter(id=item_id)
    if items.count() == 0:
        return HttpResponse(status=400, reason='Attempt to review a non existent ID: ' + item_id)

    assert items.count() == 1
    for item in items:
        # Take current review's quality and infer new values for review variables:
        #  - repetitions: quality <3 breaks the streak and resets it to 1, I think
        #  - easiness is lowered if quality is low
        #  - interval is shortened if quality is low
        sm = SMTwo(quality=quality, interval=item.interval,
                   repetitions=item.repetitions, easiness=item.easiness)

        today = datetime.date.today()

        item.interval = sm.new_interval
        item.repetitions = sm.new_repetitions
        item.easiness = sm.new_easiness
        item.next_review = today + datetime.timedelta(days=sm.new_interval)
        item.save()

    return HttpResponse()

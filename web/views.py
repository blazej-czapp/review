import datetime
import json

from  supermemo2 import SMTwo

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from web.models import ReviewItem
from django.shortcuts import redirect
from operator import attrgetter
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from web.utils import conversion_to_hyperlink
from web.logic import items_due

@login_required
@require_http_methods(["GET"])
def index(request):
    return render(request, 'web/index.html')

@login_required
@require_http_methods(["GET"])
def review_list(request):
    to_review = items_due(request.user, datetime.date.today())
    return render(request, 'web/review_list.html', {'review_items': to_review})

@login_required
@require_http_methods(["GET"])
def get_raw_review_item_data(request):
    item = ReviewItem.objects.get(added_by=request.user, id=request.GET['review_item_id'])
    data = { "caption": item.caption, "location": item.location, "notes": item.notes }
    return JsonResponse(data)

@login_required
@require_http_methods(["POST"])
def add_new_review_item(request):
    caption = request.POST['caption']

    if not caption:
        return HttpResponse(status=400, reason='caption is empty')

    # arbitrarily setting initial quality to 3
    sm = SMTwo.first_review(quality=3)

    conv = conversion_to_hyperlink(request.POST['location'])
    sanitized_location = conv + request.POST['location'] if conv is not None else request.POST['location']
    #new_repetitions is 2 at start, feels wrong
    ReviewItem.objects.create(added_by=request.user, caption=caption, location=sanitized_location,
                              is_hyperlink=conv is not None, notes=request.POST['notes'], interval=sm.interval,
                              repetitions=sm.repetitions, next_review=sm.review_date, easiness=sm.easiness)
    return HttpResponse()

@login_required
@require_http_methods(["POST"])
def edit_existing_review_item(request):
    caption = request.POST['caption']

    if not caption:
        return HttpResponse(status=400, reason=f'caption is empty')

    item = ReviewItem.objects.get(added_by=request.user, id=request.POST['review_item_id'])

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

    item = ReviewItem.objects.get(added_by=request.user, id=request.POST['review_item_id'])
    today = datetime.date.today()

    # Take current review's quality and infer new values for review variables:
    #  - repetitions: quality <3 breaks the streak and resets it to 1, I think
    #  - easiness is lowered if quality is low
    #  - interval is shortened if quality is low
    sm = SMTwo(easiness=item.easiness, interval=item.interval, repetitions=item.repetitions)
    reviewed = sm.review(quality, today)

    item.interval = reviewed.interval
    item.repetitions = reviewed.repetitions
    item.easiness = reviewed.easiness
    item.next_review = reviewed.review_date
    item.save()

    return JsonResponse({ 'items_due_count': len(items_due(request.user, today)) })

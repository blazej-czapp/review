from web.models import ReviewItem


def items_due(user, date):
    # arbitrary ordering just to keep the list stable
    return ReviewItem.objects.filter(next_review__lte=date, added_by=user).order_by('id')

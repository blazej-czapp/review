import datetime

def is_due_for_review(rep_count, last_rep_date, today):
    # review after a week, then after 2 weeks (from last review), then 4 etc.
    return last_rep_date + datetime.timedelta(weeks=2**rep_count) <= today
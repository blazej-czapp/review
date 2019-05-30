from django.test import TestCase
from django.urls import reverse

from freezegun import freeze_time
import datetime
from .models import Resource

class ReviewListTests(TestCase):
    def test_no_resources(self):
        response = self.client.get(reverse('web:index'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['resources']), 0)

    def test_res_for_review_after_week(self):
        with freeze_time("2019-05-01"):
            response = self.client.post(reverse('web:add_new_resource'), {'caption' : 'TestCaption',
                                                                          'location' : 'TestLocation',
                                                                          'notes' : 'TestNotes'})
            self.assertEqual(response.status_code, 200)
            to_review = self.client.get(reverse('web:index')).context['resources']
            self.assertEqual(len(to_review), 0)

        # nothing to review less than a week later
        with freeze_time("2019-05-04"):
            to_review = self.client.get(reverse('web:index')).context['resources']
            self.assertEqual(len(to_review), 0)

        # but appears after a week
        with freeze_time("2019-05-09"):
            to_review = self.client.get(reverse('web:index')).context['resources']
            self.assertEqual(len(to_review), 1)

    def test_review_extends_interval(self):
        with freeze_time("2019-05-01"):
            response = self.client.post(reverse('web:add_new_resource'), {'caption' : 'TestCaption',
                                                                          'location' : 'TestLocation',
                                                                          'notes' : 'TestNotes'})

        with freeze_time("2019-05-08"):
            to_review = self.client.get(reverse('web:index')).context['resources'][0]
            self.client.post(reverse('web:reviewed'), {'resource_id' : to_review.id, 'new_rep_count' : 1})

        # a week and a bit later there's still nothing
        with freeze_time("2019-05-16"):
            self.assertEqual(len(self.client.get(reverse('web:index')).context['resources']), 0)

        # but back for review after two weeks since last review
        with freeze_time("2019-05-23"):
            self.assertEqual(len(self.client.get(reverse('web:index')).context['resources']), 1)
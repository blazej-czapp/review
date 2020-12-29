from django.db import models

class Resource(models.Model):
    caption = models.TextField()
    location = models.TextField(blank=True, null=True, help_text="e.g. URL or book title")
    notes = models.TextField(blank=True, null=True, help_text="e.g. section title or book page number")

    # SuperMemo variables
    interval = models.IntegerField('Next review interval')
    repetitions = models.IntegerField('Successful review streak')
    easiness = models.FloatField('Easiness')
    next_review = models.DateField('Next review')

    def __str__(self):
        return self.caption

    def is_hyperlink(self):
        return self.location.startswith("http") or self.location.startswith("www")

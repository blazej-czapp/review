from django.db import models

class Resource(models.Model):
    caption = models.TextField()
    rep_count = models.IntegerField('Times repeated', default=0)
    last_rep_date = models.DateField('Last repetition')

    location = models.TextField(blank=True, null=True, help_text="e.g. URL or book title")
    notes = models.TextField(blank=True, null=True, help_text="e.g. section title or book page number")

    def __str__(self):
        return self.caption

    def is_hyperlink(self):
        return self.location.startswith("http") or self.location.startswith("www")

from django.db import models
from django.conf import settings

class Resource(models.Model):
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    caption = models.TextField()
    location = models.TextField(blank=True, null=True, help_text="e.g. URL or book title")
    notes = models.TextField(blank=True, null=True, help_text="e.g. section title or book page number")
    is_hyperlink = models.BooleanField(help_text="Is location a live hyperlink?")

    # SuperMemo variables
    interval = models.IntegerField('Next review interval')
    repetitions = models.IntegerField('Successful review streak')
    easiness = models.FloatField('Easiness')
    next_review = models.DateField('Next review')

    def save_model(self, request, obj, form, change):
        obj.added_by = request.user
        super().save_model(request, obj, form, change)

    def __str__(self):
        return self.caption

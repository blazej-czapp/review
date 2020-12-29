from django.contrib import admin

from .models import *

class ResourceAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        query = super().get_queryset(request)
        return query.filter(added_by=request.user)

    exclude = ['added_by']

admin.site.register(Resource, ResourceAdmin)

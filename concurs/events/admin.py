from django.contrib import admin

from events.models import EventModel, HistoryModel

admin.site.register(HistoryModel)
admin.site.register(EventModel)

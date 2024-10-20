from django.contrib import admin

from FamPay_Task.models import APIKey, FetchHistory, SearchQuery, Video

# Register your models here.
admin.site.register(Video)
admin.site.register(APIKey)
admin.site.register(FetchHistory)
admin.site.register(SearchQuery)

from django.contrib import admin

from .models import Change, Log, SharePermission, ToDo

# Register your models here.
admin.site.register(ToDo)
admin.site.register(Change)
admin.site.register(SharePermission)
admin.site.register(Log)

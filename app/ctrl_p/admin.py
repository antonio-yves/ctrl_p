from django.contrib import admin
from .models import File, Quota, Report

admin.site.register(File)
admin.site.register(Quota)
admin.site.register(Report)

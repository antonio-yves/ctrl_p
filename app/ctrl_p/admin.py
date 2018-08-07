from django.contrib import admin
from .models import File

class FileAdmin(admin.ModelAdmin):

  filter_horizontal = ('files',)
  list_display = ['name', 'status']

admin.site.register(File)

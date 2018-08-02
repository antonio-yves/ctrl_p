from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView

from .models import File

class RequirimentView(TemplateView):

    template_name = 'ctrl_p/dashboard.html'

class UploadFile(CreateView):
    model = File
    fields = ['user', 'name', 'copy', 'file']

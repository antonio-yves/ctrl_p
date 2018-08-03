from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

from .models import File
from .forms import FormFile

class RequirimentView(TemplateView):

    template_name = 'ctrl_p/dashboard.html'

class UploadFile(CreateView):
    model = File
    template_name = 'ctrl_p/upload_file.html'
    success_url = reverse_lazy('ctrl_p:success')
    fields = ['user', 'name', 'copy', 'file']

class SuccessView(TemplateView):
	template_name = 'ctrl_p/success.html'

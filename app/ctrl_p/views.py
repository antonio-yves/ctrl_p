from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView

from . import models

class DashboardView(TemplateView):

    template_name = 'ctrl_p/dashboard.html'

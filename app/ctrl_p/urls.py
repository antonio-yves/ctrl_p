# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.urls import include, path
from django.conf.urls import include, url
from django.contrib.auth import views as auth_views

from . import views as core

app_name = 'ctrl_p'

urlpatterns = [

    # Impressao
    path('solicitacao/', auth_views.LoginView.as_view(template_name='ctrl_p/dashboard.html'), name='solicitacao'),

]

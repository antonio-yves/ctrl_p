# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.urls import include, path
from django.conf.urls import include, url
from django.contrib.auth import views as auth_views

from . import views as ctrl_p

app_name = 'ctrl_p'

urlpatterns = [

    # Impressao
    path('solicitacao/', ctrl_p.RequirimentView.as_view(template_name='ctrl_p/dashboard.html'), name='solicitacao'),
    # Upload File
    path('upload-file/', ctrl_p.UploadFile.as_view(template_name='ctrl_p/upload_file.html'), name='upload-file'),
    # Success
    path('success/', ctrl_p.SuccessView.as_view(template_name='ctrl_p/success.html'), name='success'),

]

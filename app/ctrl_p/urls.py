# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.urls import include, path
from django.conf.urls import include, url
from django.contrib.auth import views as auth_views

from . import views as ctrl_p

app_name = 'ctrl_p'

urlpatterns = [

    # Impressao
    path('solicitacao/<pk>', ctrl_p.RequirimentView.as_view(template_name='ctrl_p/dashboard.html'), name='solicitacao'),

    # Upload File
    path('upload-file/', ctrl_p.UploadFile.as_view(template_name='ctrl_p/file/upload_file.html'), name='upload-file'),

    # Success
    path('success/', ctrl_p.SuccessView.as_view(template_name='ctrl_p/file/success.html'), name='success'),

    # Success Update
    path('success-update/', ctrl_p.SuccessUpdateView.as_view(template_name='ctrl_p/admin/success.html'), name='success-update'),

    # Dashboard Admin
    path('admin-printer/', ctrl_p.AdminView.as_view(template_name='ctrl_p/admin/index.html'), name='admin-printer'),

    # Search Results
    path('results/', ctrl_p.ResultsView.as_view(template_name='ctrl_p/admin/results.html'), name='results'),

    # User Details
    path('user/<pk>/details', ctrl_p.UserDetailView.as_view(template_name='ctrl_p/admin/user-details.html'), name='user-details'),

    # File Update
    path('file/<pk>/update/', ctrl_p.UpdateFileView.as_view(template_name='ctrl_p/file/file-update.html'), name='file-update'),

]

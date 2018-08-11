# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.urls import include, path
from django.conf.urls import include, url
from django.contrib.auth import views as auth_views

from . import views as ctrl_p

app_name = 'ctrl_p'

urlpatterns = [

    # Upload File
    path('user/<pk>/upload-file/', ctrl_p.UploadFile.as_view(template_name='ctrl_p/file/upload_file.html'), name='upload-file'),

    # Files Printer
    path('user/<pk>/printer', ctrl_p.PrinterView.as_view(template_name='ctrl_p/user/printer.html'), name='printer'),

    # Files Waiting
    path('user/<pk>/waiting', ctrl_p.WaitingView.as_view(template_name='ctrl_p/user/waiting.html'), name='waiting'),

    # Files Complete
    path('user/<pk>/complete', ctrl_p.CompleteView.as_view(template_name='ctrl_p/user/complete.html'), name='complete'),

    # Files Printer Admin
    path('admin/<pk>/printer', ctrl_p.AdminPrinterView.as_view(template_name='ctrl_p/admin/printer.html'), name='admin-printer'),

    # Files Waiting Admin
    path('admin/<pk>/waiting', ctrl_p.AdminWaitingView.as_view(template_name='ctrl_p/admin/waiting.html'), name='admin-waiting'),

    # Files Report Admin
    path('admin/<pk>/report', ctrl_p.AdminReportView.as_view(template_name='ctrl_p/admin/report.html'), name='admin-report'),

    # Success
    path('success/', ctrl_p.SuccessView.as_view(template_name='ctrl_p/file/success.html'), name='success'),

    # Success Update
    path('success-update/', ctrl_p.SuccessUpdateView.as_view(template_name='ctrl_p/admin/success.html'), name='success-update'),

    # Search Results
    path('search-user/', ctrl_p.ResultsView.as_view(template_name='ctrl_p/admin/results.html'), name='results'),

    # User Details
    path('user/<pk>/details', ctrl_p.UserDetailView.as_view(template_name='ctrl_p/user/details.html'), name='user-details'),

    # File Update
    path('file/<pk>/update/', ctrl_p.UpdateFileView.as_view(template_name='ctrl_p/file/file-update.html'), name='file-update'),

    # View File
    path('documentos/<pk>', ctrl_p.ViewPDF.as_view(), name='view-file')

]

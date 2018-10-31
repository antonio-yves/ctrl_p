# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.urls import include, path
from django.conf.urls import include, url
from django.contrib.auth import views as auth_views

from . import views as ctrl_p

app_name = 'ctrl_p'

urlpatterns = [

    # Upload File
    path('usuario/<pk>/upload/arquivo/', ctrl_p.UploadFile.as_view(), name='upload-file'),

    # Files Printer
    path('usuario/<pk>/printer', ctrl_p.PrinterView.as_view(template_name='ctrl_p/user/printer.html'), name='printer'),

    # Files Waiting
    path('usuario/<pk>/waiting', ctrl_p.WaitingView.as_view(template_name='ctrl_p/user/waiting.html'), name='waiting'),

    # Files Complete
    path('usuario/<pk>/complete', ctrl_p.CompleteView.as_view(template_name='ctrl_p/user/complete.html'), name='complete'),

    # Files Printer Admin
    path('administrador/<pk>/printer', ctrl_p.AdminPrinterView.as_view(template_name='ctrl_p/admin/printer.html'), name='admin-printer'),

    # Files Waiting Admin
    path('administrador/<pk>/waiting', ctrl_p.AdminWaitingView.as_view(template_name='ctrl_p/admin/waiting.html'), name='admin-waiting'),

    # Report Admin
    path('administrador/<pk>/report', ctrl_p.AdminReportView.as_view(template_name='ctrl_p/admin/report.html'), name='admin-report'),

    # Quota Admin
    path('administrador/<pk>/quota', ctrl_p.AdminQuotaView.as_view(), name='admin-quota'),

    # Success
    path('arquivo/upload/sucesso/', ctrl_p.SuccessView.as_view(template_name='ctrl_p/file/success.html'), name='success'),

    # Success Update
    path('administrador/atualizar/arquivo/sucesso', ctrl_p.SuccessUpdateView.as_view(template_name='ctrl_p/admin/success.html'), name='success-update'),

    # Search Results
    path('usuario/search/', ctrl_p.ResultsView.as_view(template_name='ctrl_p/admin/results.html'), name='results'),

    # User Details
    path('usuario/<pk>/detalhes', ctrl_p.UserDetailView.as_view(template_name='ctrl_p/user/details.html'), name='user-details'),

    # File Update
    path('arquivo/<pk>/atualizar/', ctrl_p.UpdateFileView.as_view(template_name='ctrl_p/file/file-update.html'), name='file-update'),

    # Open File
    path('arquivo/<pk>/imprimir', ctrl_p.ViewPDF.as_view(), name='view-file'),

    # Error (Insufficient Quota)
    path('administrador/cota/erro/', ctrl_p.ErrorFile.as_view(), name='error'),

    # Edit User Quota
    path('usuario/<pk>/editar/cota', ctrl_p.EditQuotaUser.as_view(), name = 'edit-quota-user'),

    # Generate Report
    path('gerar/relatorio', ctrl_p.GenerateReport.as_view(), name='generate-report'),

    # Error Report
    path('gerar/relatorio/erro', ctrl_p.ErrorReport.as_view(), name='report-error'),

    # View Report
    path('relatorio/<pk>/visualizar', ctrl_p.ViewReport.as_view(), name='report-view'),

    # Delete Report
    path('relatorio/<pk>/excluir', ctrl_p.DeleteReport.as_view(), name='report-delete'),

    # Success Report
    path('gerar/relatorio/sucesso', ctrl_p.SuccessReport.as_view(), name='report-success'),

]

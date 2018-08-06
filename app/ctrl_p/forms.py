#coding:utf-8
from __future__ import unicode_literals

from django import forms

from .models import File

class FormFile(forms.ModelForm):

    def save(self, commit = True):
        file = super(FormFile, self).save(commit=False)
        if commit:
            file.save()
        return file

    class Meta:
        model = File
        fields = ['user', 'name', 'copy', 'file']
        labels = {
            'user': 'Usuário',
            'name': 'Nome do Arquivo',
            'copy': 'Número de Cópias',
        }
        widgets = {
            'file': forms.FileInput()
        }

from django.db import models
from app.core.models import CreateUpdateModel, UUIDUser

# Model referente aos arquivos enviados para impressão
class File(CreateUpdateModel):
  STATUS = (
    (1,'Aguardando Impressão'),
    (2,'Aguardando Retirada'),
    (3,'Concluído')
  )
  user = models.ForeignKey(UUIDUser, on_delete = models.CASCADE, related_name = 'users', verbose_name = 'Usuário')
  name = models.CharField(max_length = 100, verbose_name = 'Nome')
  pages = models.IntegerField(verbose_name = 'Quantidade de Páginas do Documento')
  copy = models.IntegerField(verbose_name = 'Número de Cópias')
  file = models.FileField(upload_to = 'documents/', verbose_name = 'Arquivo')
  status = models.IntegerField(choices = STATUS, verbose_name = 'Status de Impressão', default = 1)
  uploaded = models.DateTimeField(auto_now_add = True)

  def __str__(self):
    return self.name

  class Meta:
    verbose_name = 'Arquivo'
    verbose_name_plural = 'Arquivos'

class Quota(CreateUpdateModel):
  user = models.ForeignKey(UUIDUser, on_delete = models.CASCADE, related_name = 'user', verbose_name = 'Usuário')
  quota = models.IntegerField(verbose_name = 'Cota', default = 100)
  create = models.DateTimeField(auto_now_add = True)

  def __str__(self):
    return 'Cota do Usuário: %s' % (self.user.first_name)

  class Meta:
    verbose_name = 'Cota'
    verbose_name_plural = 'Cotas'

class Report(CreateUpdateModel):
  name = models.CharField(max_length = 25, verbose_name = 'Nome')
  file = models.FileField(upload_to = 'reports/', verbose_name = 'Arquivo')
  create = models.DateTimeField(auto_now_add = True)

  def __str__(self):
    return self.name

  class Meta:
    verbose_name = 'Relatório'
    verbose_name_plural = 'Relatórios'

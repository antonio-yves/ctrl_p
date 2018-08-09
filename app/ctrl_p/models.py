from django.db import models
from app.core.models import CreateUpdateModel, UUIDUser

# Model referente aos arquivos enviados para impressão
class File(CreateUpdateModel):
  '''
  STATUS = (
    (1,'Aguardando Impressão'),
    (2,''),
    (3,'')
  )
  choices=STATUS
  '''
  user = models.ForeignKey(UUIDUser, on_delete=models.CASCADE, related_name='users', verbose_name='Usuário')
  name = models.CharField(max_length=20, verbose_name='Nome')
  copy = models.IntegerField(verbose_name='Número de Cópias')
  file = models.FileField(upload_to='documents/', verbose_name='Arquivo')
  status = models.IntegerField(verbose_name='Status de Impressão', default=1)
  uploaded = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.name

  class Meta:
    verbose_name = 'Arquivo'
    verbose_name_plural = 'Arquivos'

# Garag3m: ctrl_p

Projeto de requerimento de impressão desenvolvido pela Garag3m.

# Template Base

O Template utilizado no desenvolvimento foi o AdminLTE <https://github.com/ColorlibHQ/AdminLTE>

## Apps

O projeto é composto pela aplicação *core* e *ctrl_p* que são compostas basicamente pelas classes *CreateUpdateModel*, *UUIDUser*, *Quota*, *Report* e *File*.   

### CreateUpdateModel

Classe composta basicamente pelos atributos de data de criação (created_at) e data da última atualização (updated_at). Além disso ela define um *id* como sendo UUID.

```python
class CreateUpdateModel(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField('criado em', auto_now_add=True)
    updated_at = models.DateTimeField('atualizado em', auto_now=True)

    class Meta:
        abstract = True
```

### UUIDUser

Classe que herda da classe AbstractUser, sendo utilizada para sobrescrever a classe User do Django. Como diferencial ela possui apenas os atributos de cpf, matrícula e imagem do profile do usuário.

```python
class UUIDUser(AbstractUser):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    groups = models.ManyToManyField(Group, blank=True, related_name="uuiduser_set", related_query_name="user")
    user_permissions = models.ManyToManyField(Permission, blank=True, related_name="uuiduser_set", related_query_name="user")

    # core
    cpf = models.CharField(max_length=11, null=True, blank=True, verbose_name="CPF")
    registration = models.CharField(max_length=100, null=True, blank=True, verbose_name="matrícula")

    # picture
    picture = models.ImageField(null=False, blank=True, verbose_name='picture', upload_to='accounts/%Y/%m/%d')
    picture_thumb = ImageSpecField(source='picture', processors=[ResizeToFill(200, 200)], format='JPEG', options={'quality': 60})

    def __str__(self):
        return self.first_name

    class Meta:
        verbose_name = 'usuário'
        verbose_name_plural = 'usuários'
```

Você pode ver no arquivo settings.py a definição da classe UUIDUser como classe de usuário padrão.

```python
AUTH_USER_MODEL = 'core.UUIDUser'
```
### Quota
Classe composta basicamente pelos atributos: usuário (user), cota (quota), used (usado) e create (criado).
```python
class Quota(CreateUpdateModel):
  user = models.ForeignKey(UUIDUser, on_delete = models.CASCADE, related_name = 'user', verbose_name = 'Usuário')
  quota = models.IntegerField(verbose_name = 'Cota', default = 100)
  used = models.IntegerField(verbose_name='Cota Usada', default=0)
  create = models.DateTimeField(auto_now_add = True)

  def __str__(self):
    return 'Cota do Usuário: %s' % (self.user.first_name)

  class Meta:
    verbose_name = 'Cota'
    verbose_name_plural = 'Cotas'
```
### Report
Classe composta basicamente pelos atributos: name (nome), min_date(data inicial), max_date (data final), pages (nº de páginas impressas) e create (criado).
```python
class Report(CreateUpdateModel):
  name = models.CharField(max_length = 25, verbose_name = 'Nome')
  min_date = models.DateField(verbose_name='Data Inicial')
  max_date = models.DateField(verbose_name='Data Final')
  pages = models.IntegerField(verbose_name='Páginas Impressas')
  create = models.DateTimeField(auto_now_add = True)

  def __str__(self):
    return self.name

  class Meta:
    verbose_name = 'Relatório'
    verbose_name_plural = 'Relatórios'
```

### File
Classe composta basicamente pelos atributos: usuário (user), nome do arquivo (name), quantidade de cópiad (copy), o arquivo para ser impresso (file) e a data de upload (uploaded).
 ```python
class File(CreateUpdateModel):
    user = models.ForeignKey(UUIDUser, on_delete=models.CASCADE, related_name='users', verbose_name='Usuário')
    name = models.CharField(max_length=20, verbose_name='Nome')
    copy = models.IntegerField(verbose_name='Número de Cópias')
    file = models.FileField(upload_to='documents/', verbose_name='Arquivo')
    uploaded = models.DateTimeField(auto_now_add=True)
     def __str__(self):
        return self.name
     class Meta:
        verbose_name = 'Arquivo'
        verbose_name_plural = 'Arquivos'
```

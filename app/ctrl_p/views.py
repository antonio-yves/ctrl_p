from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy

from . import models

from .models import File
from .forms import FormFile
from app.core.models import UUIDUser

# Upload File
#--------------------------
class UploadFile(CreateView):
	'''
	Classe responsável por realizar o upload e salvamento do arquivo no banco de dados
	'''
	model = File # Criando Model da classe com base no model File
	template_name = 'ctrl_p/file/upload_file.html' # Informando a classe o template que será utilizado para renderizar os dados
	success_url = reverse_lazy('ctrl_p:success') # Tela que o usuário será enviado se sua requisição for concluída com êxito
	fields = ['user', 'name', 'copy', 'file'] # Formulário que será utilizado no template para realizar o upload do arquivo

# Success
#-----------------------------
class SuccessView(TemplateView):
	'''
	Classe com o template success, que será renderizado quando o upload do arquivo for concluído com êxito
	'''
	template_name = 'ctrl_p/file/success.html' # Definindo o template de renderização da classe

# Super User View
#------------------------
class AdminView(ListView):
	'''
	Classe responsável por renderizar os dados que serão visualizados pelo usuário administrador
	'''
	model = File # Criando Model da classe com base no model File
	template_name = 'ctrl_p/admin/index.html' # Informando a classe o template que será utilizado para renderizar os dados

	def get_context_data(self, **kwargs):
		kwargs['files_print'] = models.File.objects.filter(status = 1).order_by('-uploaded') # Pegando do banco de dados os arquivos que estão aguardando para serem impressos
		kwargs['files_waiting'] = models.File.objects.filter(status = 2).order_by('-uploaded') # Pegando do banco de dados os arquivos que estão aguardando para serem impressos
		return super(AdminView, self).get_context_data(**kwargs) # Retornando os dados para o template, para serem mostrados ao usuário

# Results View displayed only by Super User
#------------------------
class ResultsView(ListView):
	'''
	Classe responsável por listar os resultados da pesquisa realizada pelo usuário administrador
	'''
	model = UUIDUser # Criando Model da classe com base no model UUIDUser do app core
	template_name = 'ctrl_p/admin/results.html' # Informando a classe o template que será utilizado para renderizar os dados

	def get_queryset(self, **kwargs):
		if 'q' in self.request.GET: # Verificando que a variável 'q' foi passada durante a solicitação
			object_list = self.model.objects.filter(first_name__icontains = self.request.GET['q']) # Pegando do banco de dados os usuários que foram encontrados a partir do valor passado na requisição
		else: # Caso não tenha sido passada durante a solicitação
			object_list = self.model.objects.all() # Pegamos no banco de dados todos os usuários cadastrados
		return object_list # Retornando os dados para o template, para serem mostrados ao usuário

# Profile User
#------------------------------- 
class UserDetailView(DetailView):
	'''
	Classe responsável por mostrar ao usuário administrador os dados de um usuário
	'''
	model = UUIDUser # Criando Model da classe com base no model UUIDUser do app core
	template_name = 'ctrl_p/user/user-details.html' # Informando a classe o template que será utilizado para renderizar os dados

	def get_context_data(self, **kwargs):
		kwargs['files_print'] = models.File.objects.filter(user = self.object.id, status = 1).order_by('-uploaded') # Pegando do banco de dados os arquivos que estão aguardando para serem impressos e que estão relacionados ao usuário atual
		kwargs['files_waiting'] = models.File.objects.filter(user = self.object.id, status = 2).order_by('-uploaded') # Pegando do banco de dados os arquivos que estão aguardando para serem retirados e que estão relacionados ao usuário atual
		kwargs['files_complete'] = models.File.objects.filter(user = self.object.id, status = 3).order_by('-uploaded') # Pegando do banco de dados os arquivos que estão concluídos e que estão relacionados ao usuário atual
		return super(UserDetailView, self).get_context_data(**kwargs) # Retornando os dados para o template, para serem mostrados ao usuário

# Normal User View
#---------------------------------
class RequirimentView(UserDetailView): # Criamos a classe herdando de UserDetailView para receber todos os seus atributos
	'''
	Classe responsável por mostrar ao usuário seus arquivos
	'''
	template_name = 'ctrl_p/dashboard.html' # Sobrescrevemos o template da classe mãe


from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from django.views import View
from django.http import HttpResponse

from . import models

from .models import File
from .forms import FormFile
from app.core.models import UUIDUser

# View do usuário comun com os arquivos aguardando impressão
#-----------------------------
class PrinterView(DetailView):
	model = UUIDUser
	template_name = 'ctrl_p/user/printer.html'

	def get_context_data(self, **kwargs):
		kwargs['files_print'] = models.File.objects.filter(user = self.object.id, status = 1).order_by('-uploaded')
		return super(PrinterView, self).get_context_data(**kwargs)

# View do usuário comun com os arquivos aguardando retirada
#-----------------------------
class WaitingView(DetailView):
	model = UUIDUser
	template_name = 'ctrl_p/user/waiting.html'

	def get_context_data(self, **kwargs):
		kwargs['files_waiting'] = models.File.objects.filter(user = self.object.id, status = 2).order_by('-uploaded')
		return super(WaitingView, self).get_context_data(**kwargs)

# View do usuário comun com os arquivos concluídos
#------------------------------
class CompleteView(DetailView):
	model = UUIDUser
	template_name = 'ctrl_p/user/complete.html'

	def get_context_data(self, **kwargs):
		kwargs['files_complete'] = models.File.objects.filter(user = self.object.id, status = 3).order_by('-uploaded')
		return super(CompleteView, self).get_context_data(**kwargs)

# View do usuário administrador com os arquivos aguardando impressão
#--------------------------------
class AdminPrinterView(ListView):
	'''
	Classe responsável por renderizar os arquivos que estão aguardando para serem impressos. Visualização do Usuário Administrador
	'''
	model = File # Criando Model da classe com base no model File
	template_name = 'ctrl_p/admin/printer.html' # Informando a classe o template que será utilizado para renderizar os dados

	def get_context_data(self, **kwargs):
		kwargs['files_print'] = models.File.objects.filter(status = 1).order_by('-uploaded') # Pegando do banco de dados os arquivos que estão aguardando para serem impressos
		return super(AdminPrinterView, self).get_context_data(**kwargs) # Retornando os dados para o template, para serem mostrados ao usuário

# View do usuário administrador com os arquivos aguardando retirada
#--------------------------------
class AdminWaitingView(ListView):
	'''
	Classe responsável por renderizar os arquivos que estão aguardando para serem retirados pelo solicitador. Visualização do Usuário Administrador
	'''
	model = File # Criando Model da classe com base no model File
	template_name = 'ctrl_p/admin/waiting.html' # Informando a classe o template que será utilizado para renderizar os dados

	def get_context_data(self, **kwargs):
		kwargs['files_waiting'] = models.File.objects.filter(status = 2).order_by('-uploaded') # Pegando do banco de dados os arquivos que estão aguardando para serem impressos
		return super(AdminWaitingView, self).get_context_data(**kwargs) # Retornando os dados para o template, para serem mostrados ao usuário

# View do usuário administrador onde ele poderá gerar relatórios de uso
#-----------------------------------
class AdminReportView(TemplateView):
	template_name = 'ctrl_p/admin/report.html'

# View para consulta de dados do usuário, será mostrada quando o administrador realizar
# alguma pesquisa e selecionar um usuário dos resultados apresentados.
#------------------------------- 
class UserDetailView(DetailView):
	'''
	Classe responsável por mostrar ao usuário administrador os dados de um usuário
	'''
	model = UUIDUser # Criando Model da classe com base no model UUIDUser do app core
	template_name = 'ctrl_p/user/details.html' # Informando a classe o template que será utilizado para renderizar os dados

	def get_context_data(self, **kwargs):
		kwargs['files_print'] = models.File.objects.filter(user = self.object.id, status = 1).order_by('-uploaded') # Pegando do banco de dados os arquivos que estão aguardando para serem impressos e que estão relacionados ao usuário atual
		kwargs['files_waiting'] = models.File.objects.filter(user = self.object.id, status = 2).order_by('-uploaded') # Pegando do banco de dados os arquivos que estão aguardando para serem retirados e que estão relacionados ao usuário atual
		kwargs['files_complete'] = models.File.objects.filter(user = self.object.id, status = 3).order_by('-uploaded') # Pegando do banco de dados os arquivos que estão concluídos e que estão relacionados ao usuário atual
		return super(UserDetailView, self).get_context_data(**kwargs) # Retornando os dados para o template, para serem mostrados ao usuário

# View responsável pelo carregamento do arquivo para impressão
#----------------------------
class UploadFile(CreateView):
	'''
	Classe responsável por realizar o upload e salvamento do arquivo no banco de dados
	'''
	model = File # Criando Model da classe com base no model File
	template_name = 'ctrl_p/file/upload_file.html' # Informando a classe o template que será utilizado para renderizar os dados
	success_url = reverse_lazy('ctrl_p:success') # Tela que o usuário será enviado se sua requisição for concluída com êxito
	fields = ['user', 'name', 'copy', 'file'] # Formulário que será utilizado no template para realizar o upload do arquivo

# View da mensagem sucesso, será mostrada quando o usuário comun realizar o upload de um arquivo para impressão
#-------------------------------
class SuccessView(TemplateView):
	'''
	Classe com o template success, que será renderizado quando o upload do arquivo for concluído com êxito
	'''
	template_name = 'ctrl_p/file/success.html' # Definindo o template de renderização da classe

# View da mensagem sucesso, será mostrada quando o usuário administrador realizar uma atualização no status do arquivo
#-------------------------------------
class SuccessUpdateView(TemplateView):
	'''
	Classe com o template success, que será renderizado quando o arquivo for atualizado com êxito
	'''
	template_name = 'ctrl_p/admin/success.html' # Definindo o template de renderização da classe

# View que renderizará os resultados da pesquisa realizada pelo usuário administrador
#---------------------------
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

# View que renderizará um arquivo já existente no banco e dará a opção de atualizar o status do arquivo
#--------------------------------
class UpdateFileView(UpdateView):
	'''
	Classe responsável por realizar atualização no model file
	'''
	model = File # Criando Model da classe com base no model File
	template_name = 'ctrl_p/file/file-update.html' # Informando a classe o template que será utilizado para renderizar os dados
	success_url = reverse_lazy('ctrl_p:success-update') # Tela que o usuário será enviado se sua requisição for concluída com êxito
	fields = ['user', 'name', 'copy', 'file', 'status'] # Formulário que será utilizado no template para realizar o upload do arquivo

# View que renderiza o arquivo PDF na tela do navegador, para os usuários poderem visualizar o arquivo no próprio navegador
#-------------------
class ViewPDF(View):
	def get(self, request, pk):
		kwargs = models.File.objects.filter(id = pk)
		with open('uploads/%s' % kwargs[0].file, 'rb') as pdf:
			response = HttpResponse(pdf.read(), content_type='application/pdf')
			response['Content-Disposition'] = 'inline; filename="some_file.pdf"'
			pdf.close
			return response
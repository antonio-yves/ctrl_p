from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from django.views import View
from django.http import HttpResponse
from . import models
from . import functions
from .models import File, Quota
from .forms import FormFile
from app.core.models import UUIDUser
from .tasks import definir_cota, aviso_cotas
from datetime import datetime, timedelta
from django.utils import timezone

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

# View do usuário administrador onde ele poderá definir cotas de uso
#----------------------------------
class AdminQuotaView(View):
	def get(self, request, pk):
		quota = models.Quota.objects.all()
		if len(quota) == 0:
			return render(request, 'ctrl_p/admin/quota.html')
		return render(request, 'ctrl_p/admin/quota.html', {'erro': "A cota para esse mês já foi definida. Quando for necessário definir cotas novamente, você receberá um aviso no seu e-mail."})

	def post(self, request, pk):
		users = UUIDUser.objects.all()
		agora = timezone.now()
		depois = agora + timedelta(days = 30)
		if 'cota' in request.POST: 
			if int(request.POST.get('cota')) <= 0:
				return render(request, 'ctrl_p/admin/quota.html', {'mensagem': 'O valor da cota não pode ser negativo, ou igual a zero!'})
			definir_cota.apply_async([int(request.POST.get('cota'))])
			aviso_cotas.apply_async(eta = depois)
			return render(request, 'ctrl_p/admin/quota_success.html')
		elif 'ilimitada' in request.POST:
			definir_cota.apply_async([int(request.POST.get('ilimitada'))])
			aviso_cotas.apply_async(eta = depois)
			return render(request, 'ctrl_p/admin/quota_success.html')
		else:
			pass

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
		kwargs['quota'] = models.Quota.objects.filter(user = self.object.id).first()
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
	form_class = FormFile # Formulário que será utilizado no template para realizar o upload do arquivo

	def form_valid(self, form):
		obj = form.save(commit=False)
		cota = Quota.objects.filter(user = obj.user).first()
		if cota.quota == (-1):
			pass
		elif cota.quota > 0:
			if cota.quota >= obj.copy:
				cota.quota -= obj.copy
				cota.save()
			else:
				return redirect('ctrl_p:error')
		else:
			return redirect('ctrl_p:error')
		obj.save()
		return super(UploadFile, self).form_valid(form)

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
			object_list = self.model.objects.all().exclude(id = self.request.user.id) # Pegamos no banco de dados todos os usuários cadastrados
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
			response['Content-Disposition'] = 'inline; filename="%s.pdf"' % kwargs[0].name
			pdf.close
			return response

# View responsável por gerar os relatórios do usuário Administrador
#--------------------------
class GenerateReport(View):
	pass

class Error(TemplateView):
	template_name = 'ctrl_p/file/error.html'

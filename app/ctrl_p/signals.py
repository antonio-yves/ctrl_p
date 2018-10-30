from django.db.models.signals import post_save
from django.core.mail import EmailMessage
from django.core import mail
from django.dispatch import receiver

from .models import File

from app.core.models import UUIDUser

connection = mail.get_connection()
connection.open()

def file_create_post_save(sender, instance, created, **kwargs):
	user_adm = UUIDUser.objects.filter(is_staff=True).first()
	if created:
		email_user = mail.EmailMessage(
			'Arquivo Enviado com Sucesso - Status Atual "Aguradando Impressão"',
			'Caro, %s.\n\nInformamos que o arquivo "%s" foi recebido com sucesso, logo ele será impresso e você poderá pegar o arquivo pronto na mecanografia.\n\nAtenciosamente,\n%s\n\n\n\nEssa mensagem é automática, ok? Não é pra responder esse e-mail.' % (instance.user.first_name, instance.name, user_adm.first_name),
			'carlosabc436@gmail.com',
			[instance.user.email],
			connection=connection,
			)
		email_user.send()
		email_adm = mail.EmailMessage(
			'Novo Arquivo Aguradando Impressão',
			'O usuário %s enviou um novo arquivo para impressão.\n\nDetalhes da Solicitação:\nNome do Arquivo: %s\nQuantidade de Páginas: %i\nQuantidade de Cópias: %i\n\n\n\nEssa mensagem é automática, ok? Não é pra responder esse e-mail.' % (instance.user.first_name, instance.name, instance.pages, instance.copy),
			'carlosabc436@gmail.com',
			[user_adm.email],
			connection = connection,
			)
		email_adm.send()
		connection.close()
	else:
		if instance.status == 2:
			email = mail.EmailMessage(
				'O Status do Seu Arquivo Foi Alterado - Status Atual "Aguardando Retirada"',
				'Caro, %s.\nO status do arquivo "%s" foi alterado para "Aguardando Retirada", diriga-se a mecanografia e retire seu arquivo impresso.\n\nAtenciosamente,\n%s\n\n\n\nEssa mensagem é automática, ok? Não é pra responder esse e-mail.' % (instance.user.first_name, instance.name, user_adm.first_name),
				'carlosabc436@gmail.com',
				[instance.user.email],
				connection=connection,
				)
			email.send()
			connection.close()
		else:
			email = mail.EmailMessage(
				'O Status do Seu Arquivo Foi Alterado - Status Atual "Concluído"',
				'Caro, %s.\nO status do arquivo "%s" foi alterado para "Concluído".\n\nAtenciosamente,\n%s\n\n\n\nEssa mensagem é automática, ok? Não é pra responder esse e-mail.' % (
				instance.user.first_name, instance.name, user_adm.first_name),
				'carlosabc436@gmail.com',
				[instance.user.email],
				connection=connection,
			)
			email.send()
			connection.close()

post_save.connect(file_create_post_save, sender=File)
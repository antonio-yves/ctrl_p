from django.db.models.signals import post_save
from django.core.mail import EmailMessage
from django.core import mail
from django.dispatch import receiver

from .models import File

from app.core.models import UUIDUser

connection = mail.get_connection()
connection.open()

def file_create_post_save(sender, instance, created, **kwargs):
	if created:
		user_adm = UUIDUser.objects.filter(is_staff = True)
		email_user = mail.EmailMessage(
			'Arquivo enviado com sucesso',
			'Seu arquivo foi recebido com sucesso',
			'carlosabc436@gmail.com',
			[instance.user.email],
			connection=connection,
			)
		email_user.send()
		email_adm = mail.EmailMessage(
			'Novo arquivo aguradando impressão',
			'Um usuário enviou um novo arquivo',
			'carlosabc436@gmail.com',
			[user_adm[0].email],
			connection = connection,
			)
		email_adm.send()
		connection.close()
	else:
		email = mail.EmailMessage(
			'Status do arquivo alterado',
			'O status do seu arquivo foi alterado',
			'carlosabc436@gmail.com',
			[instance.user.email],
			connection=connection,
			)
		email.send()
		connection.close()

post_save.connect(file_create_post_save, sender=File)
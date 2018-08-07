from django.db.models.signals import post_save
from django.core.mail import EmailMessage
from django.core import mail
from django.dispatch import receiver

from .models import File

connection = mail.get_connection()
connection.open()

def file_create_post_save(sender, instance, created, **kwargs):
	if created:
		email = mail.EmailMessage(
			'Arquivo enviado com sucesso',
			'Seu arquivo foi recebido com sucesso',
			'carlosabc436@gmail.com',
			['yvissousa@gmail.com'],
			connection=connection,
			)
		email.send()
		connection.close()
	else:
		email = mail.EmailMessage(
			'Status do arquivo alterado',
			'O status do seu arquivo foi alterado',
			'carlosabc436@gmail.com',
			['yvissousa@gmail.com'],
			connection=connection,
			)
		email.send()
		connection.close()


post_save.connect(file_create_post_save, sender=File)
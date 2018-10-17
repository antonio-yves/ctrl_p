# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .models import Quota
from app.core.models import UUIDUser
from django.core.mail import EmailMessage
from django.core import mail
from django.dispatch import receiver

@shared_task
def definir_cota(cota):
	connection = mail.get_connection()
	connection.open()
	users = UUIDUser.objects.all().exclude(is_staff = True)
	if len(users) != 0:
		for user in users:
			quota = Quota(user = user, quota = cota)
			quota.save()
		email = mail.EmailMessage(
			'Cota Definida',
			'A cota do mês foi definida com sucesso! \nQuando for necessário definir cota novamente, você receberá um e-mail.',
			'carlosabc436@gmail.com',
			['yvissousa@gmail.com'],
			connection=connection,
		)
		email.send()
		connection.close()
		return True
	email = mail.EmailMessage(
	'Cota Não Definida',
	'A cota do mês não foi definida com sucesso, pois não há usuários cadastrados no sistema! \nCadastre usuários para conseguir definir contas.',
	'carlosabc436@gmail.com',
	['yvissousa@gmail.com'],
	connection=connection,
	)
	email.send()
	connection.close()
	return False

@shared_task
def aviso_cotas():
	connection = mail.get_connection()
	connection.open()
	email = mail.EmailMessage(
	'Defina a cota mensal',
	'A cota do mês expirou, acesse o sistema e defina uma nova cota!',
	'carlosabc436@gmail.com',
	['yvissousa@gmail.com'],
	connection=connection,
	)
	email.send()
	connection.close()


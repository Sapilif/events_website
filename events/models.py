from django.db import models
from django.contrib.auth.models import User


class Event(models.Model):
	name = models.CharField('Nume eveniment', max_length=120)
	description = models.TextField(blank=False)
	location = models.CharField('Locatie', null=False, blank=False, max_length=200)
	eveniment_image = models.ImageField(null=True, blank=True, upload_to="images/")
	organiser = models.ForeignKey(User, blank=False, null=False, on_delete=models.CASCADE)
	eveniment_date = models.DateTimeField('Data eveniment', blank=False, null=False)
	eveniment_create_date = models.DateTimeField('Data creare eveniment', blank=False, null=False)
	tickets = models.TextField(blank=False)
	initial_tickets = models.TextField(blank=False)
	ticket_price = models.IntegerField(blank=False, null=False)
	prediction_image = models.ImageField(null=True, blank=True, upload_to="images/")
	predicted = models.BooleanField('Predictie vanzare', default = False)
	prediction_text = models.TextField(blank=True)

	def __str__(self):
		return self.name


class Ticket(models.Model):
	eveniment = models.ForeignKey(Event, blank=False, null=True, on_delete=models.CASCADE)
	user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
	nume = models.CharField('Nume', max_length=120)
	prenume = models.CharField('Prenume', max_length=120)
	is_gift = models.BooleanField('Cadou', default = False)
	sale_date = models.DateField('Data vanzare bilet', blank=True, null=True)

	def __str__(self):
		return self.eveniment.name

class Friendship(models.Model):
	user1 = models.ForeignKey(User, blank=False, null=False, on_delete=models.CASCADE, related_name='user1_prietenie')
	user2 = models.ForeignKey(User, blank=False, null=False, on_delete=models.CASCADE, related_name='user2_prietenie')

	def __str__(self):
		return self.user1.username

class FriendRequest(models.Model):
	user1 = models.ForeignKey(User, blank=False, null=False, on_delete=models.CASCADE, related_name='user1_friendrequest')
	user2 = models.ForeignKey(User, blank=False, null=False, on_delete=models.CASCADE, related_name='user2_friendrequest')

	def __str__(self):
		return self.user1.username

class AppUser(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	funds = models.IntegerField(blank=True, null=True, default=0)
	role = models.CharField('Role', max_length=120, default='user')

	def __str__(self):
		return self.user.username





from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
	name = models.CharField(max_length=50, blank=True, null=False)
	description = models.TextField(blank=False, null=False)
	status = models.BooleanField(default=False)

	def __str__(self):
		return self.name

class Journal(models.Model):
	owner = models.OneToOneField(User, null=True, on_delete=models.SET_NULL)
	title = models.TextField(blank=True, null=True)
	notes = models.TextField(blank=False, null=False)
	date_created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.owner.username
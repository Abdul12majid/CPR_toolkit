from django.db import models
from django.utils import timezone
from datetime import timedelta

# Create your models here.

class Status(models.Model):
	name = models.CharField(max_length=50, blank=True, null=False)

	def __str__(self):
		return self.name

class RelyInvoice(models.Model):
	dispatch_number = models.CharField(max_length=50, blank=True, null=True)
	status = models.ForeignKey(Status, null=True, blank=True, on_delete=models.SET_NULL)
	customer = models.CharField(max_length=50, blank=True, null=True)
	date_received = models.DateField(default=timezone.now)  # Date the invoice was received
	date_invoiced = models.DateField(default=timezone.now)  # Date the invoice was invoiced
	note = models.TextField(blank=False, null=False)
	amount = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)

	def __str__(self):
		return self.customer + " " + self.dispatch_number

class RelyProcessed(models.Model):
	dispatch_number = models.CharField(max_length=50, blank=True, null=True)
	status = models.ForeignKey(Status, null=True, blank=True, on_delete=models.SET_NULL)
	customer = models.CharField(max_length=50, blank=True, null=True)
	date_received = models.DateField(default=timezone.now)  # Date the invoice was received
	date_invoiced = models.DateField(default=timezone.now)  # Date the invoice was invoiced
	note = models.TextField(blank=False, null=False)
	amount = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)

	class Meta:
		verbose_name_plural = "RelyProcessed"

	def __str__(self):
		return self.customer + " " + self.dispatch_number

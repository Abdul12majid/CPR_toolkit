from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum, Avg
from django.utils import timezone

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
	date_created = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.owner.username


class Invoice(models.Model):
    dispatch_no = models.CharField(max_length=50, blank=True, null=False)
    name = models.CharField(max_length=50, blank=True, null=False)
    invoiced_amount = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def total(self):
        return Invoice.objects.aggregate(total=Sum('invoiced_amount'))['total'] or 0

    def seven_day_avg(self):
        seven_days_ago = now() - timedelta(days=7)
        return Invoice.objects.filter(created_at__gte=seven_days_ago).aggregate(
            avg=Avg('invoiced_amount')
        )['avg'] or 0

    def thirty_day_avg(self):
        thirty_days_ago = now() - timedelta(days=30)
        return Invoice.objects.filter(created_at__gte=thirty_days_ago).aggregate(
            avg=Avg('invoiced_amount')
        )['avg'] or 0

    def __str__(self):
        return f"{self.name} - {self.dispatch_no}"

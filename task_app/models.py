from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum, Avg
from django.utils import timezone

# Create your models here.
class Task(models.Model):
	description = models.TextField(blank=False, null=False)
	status = models.BooleanField(default=False)

	def __str__(self):
		return str(self.status)

class Belle_Task(models.Model):
    description = models.TextField(blank=False, null=False)
    status = models.BooleanField(default=False)

    def __str__(self):
        return str(self.status)

class Marvin_Task(models.Model): 
    description = models.TextField(blank=False, null=False)
    status = models.BooleanField(default=False)

    def __str__(self):
        return str(self.status)

class Journal(models.Model):
	owner = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
	title = models.TextField(blank=True, null=True)
	notes = models.TextField(blank=False, null=False)
	date_created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.owner.username


class Invoice(models.Model):
    dispatch_no = models.CharField(max_length=50, blank=True, null=False)
    name = models.CharField(max_length=50, blank=True, null=False)
    invoiced_amount = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    created_at = models.DateField(default=timezone.now)
    date_received = models.DateField(default=timezone.now)
    days_difference = models.IntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # Calculate the difference only if both dates are set
        if self.created_at and self.date_received:
            self.days_difference = (self.date_received - self.created_at).days
        else:
            self.days_difference = None
        
        # Ensure the dates are timezone-aware and converted to Los Angeles time
        if not self.created_at:
            self.created_at = timezone.now().astimezone(timezone.get_current_timezone()).date()
        if not self.date_received:
            self.date_received = timezone.now().astimezone(timezone.get_current_timezone()).date()
        
        super().save(*args, **kwargs)

    def total(self):
        return Invoice.objects.aggregate(total=Sum('invoiced_amount'))['total'] or 0

    def seven_day_avg(self):
        seven_days_ago = timezone.now() - timedelta(days=7)
        return Invoice.objects.filter(created_at__gte=seven_days_ago).aggregate(
            avg=Avg('invoiced_amount')
        )['avg'] or 0

    def thirty_day_avg(self):
        thirty_days_ago = timezone.now() - timedelta(days=30)
        return Invoice.objects.filter(created_at__gte=thirty_days_ago).aggregate(
            avg=Avg('invoiced_amount')
        )['avg'] or 0

    def __str__(self):
        return f"{self.name} - {self.dispatch_no}"
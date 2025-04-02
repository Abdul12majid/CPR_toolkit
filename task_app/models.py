from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum, Avg, F
from django.utils import timezone
from datetime import timedelta

# Create your models here.

class Work_Journal(models.Model):
    description = models.TextField(blank=False, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.description)

class Task(models.Model):
    description = models.TextField(blank=False, null=False)
    status = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.description)

class Belle_Task(models.Model):
    description = models.TextField(blank=False, null=False)
    status = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.description)

class Marvin_Task(models.Model): 
    description = models.TextField(blank=False, null=False)
    status = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.description)

class Journal(models.Model):
	owner = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
	title = models.TextField(blank=True, null=True)
	notes = models.TextField(blank=False, null=False)
	date_created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.notes

class Ebay(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    tracking_number = models.CharField(max_length=200, blank=True, null=True)
    order_number = models.CharField(default="0.0", max_length=200, blank=True, null=True)
    link = models.CharField(max_length=500, blank=True, null=True)
    amount = models.CharField(max_length=500, blank=True, null=True)
    date_pushed = models.DateField(default=timezone.now)
    date_updated = models.DateField(default=timezone.now)
    delivery_time = models.CharField(max_length=200, blank=True, null=True)
    transaction_date = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Ebay"

    def __str__(self):
        return self.name + " " + self.order_number

class Merchant(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    tracking_number = models.CharField(max_length=200, blank=True, null=True)
    order_number = models.CharField(default="0.0", max_length=200, blank=True, null=True)
    link = models.CharField(max_length=500, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_pushed = models.DateField(default=timezone.now)
    date_updated = models.DateField(default=timezone.now)
    delivery_time = models.CharField(max_length=200, blank=True, null=True)
    transaction_date = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Merchant"

    def __str__(self):
        return self.name + " " + self.order_number

class Today_order(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    tracking_number = models.CharField(max_length=200, blank=True, null=True)
    order_number = models.CharField(max_length=200, blank=True, null=True)
    link = models.CharField(max_length=500, blank=True, null=True)
    date_pushed = models.DateField(default=timezone.now)

    class Meta:
        verbose_name_plural = "Today Order"

    def __str__(self):
        return self.name + " " + self.order_number


class Invoice(models.Model):
    dispatch_no = models.CharField(max_length=50, blank=True, null=False)
    name = models.CharField(max_length=50, blank=True, null=False)
    invoiced_amount = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    created_at = models.DateField(default=timezone.now)  # Date the work order was created
    date_received = models.DateField(default=timezone.now)  # Date the invoice was received
    days_difference = models.IntegerField(blank=True, null=True)  # Days between created_at and date_received

    def save(self, *args, **kwargs):
        # Skip days_difference calculation if invoiced_amount is 0
        if self.invoiced_amount == 0:
            self.days_difference = None
        else:
            # Calculate the difference only if both dates are set
            if self.created_at and self.date_received:
                self.days_difference = (self.created_at - self.date_received).days
                
                # If days_difference is 0, set it to 1
                if self.days_difference == 0:
                    self.days_difference = 1
            else:
                self.days_difference = None
        
        # Ensure the dates are timezone-aware and converted to Los Angeles time
        if not self.created_at:
            self.created_at = timezone.now().astimezone(timezone.get_current_timezone()).date()
        if not self.date_received:
            self.date_received = timezone.now().astimezone(timezone.get_current_timezone()).date()
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.dispatch_no}"

    @classmethod
    def average_days_to_invoice(cls, days):
        """
        Calculate the average days to invoice for a given time period.
        :param days: Number of days to look back (e.g., 7 for past week, 30 for past month).
        :return: Average days to invoice for the given period.
        """
        start_date = timezone.now().date() - timedelta(days=days)
        return cls.objects.filter(created_at__gte=start_date).aggregate(
            avg_days=Avg(F('date_received') - F('created_at'))
        )['avg_days'] or 0

    @classmethod
    def past_week_avg(cls):
        """Average days to invoice for the past week."""
        return cls.average_days_to_invoice(7)

    @classmethod
    def past_month_avg(cls):
        """Average days to invoice for the past month."""
        return cls.average_days_to_invoice(30)

    @classmethod
    def past_six_months_avg(cls):
        """Average days to invoice for the past 6 months."""
        return cls.average_days_to_invoice(180)

    @classmethod
    def past_year_avg(cls):
        """Average days to invoice for the past 12 months."""
        return cls.average_days_to_invoice(365)

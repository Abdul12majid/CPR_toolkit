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
        return f"{self.customer} {self.dispatch_number}"

    @property
    def days_difference(self):
        """
        Calculate the difference in days between date_received and date_invoiced.
        Returns None if either date is missing or if amount is 0.
        """
        if self.amount == 0:
            return None  # Skip calculation if amount is 0

        if self.date_received and self.date_invoiced:
            difference = (self.date_invoiced - self.date_received).days
            # If difference is 0, set it to 1
            return 1 if difference == 0 else difference
        return None

    def save(self, *args, **kwargs):
        # Ensure the dates are set to today's date if they are not provided
        if not self.date_invoiced:
            self.date_invoiced = timezone.now().date()
        if not self.date_received:
            self.date_received = timezone.now().date()
        
        super().save(*args, **kwargs)

class RelyCompleted(models.Model):
	dispatch_number = models.CharField(max_length=50, blank=True, null=True)
	status = models.ForeignKey(Status, null=True, blank=True, on_delete=models.SET_NULL)
	customer = models.CharField(max_length=50, blank=True, null=True)
	date_received = models.DateField(default=timezone.now)  # Date the invoice was received
	date_invoiced = models.DateField(default=timezone.now)  # Date the invoice was invoiced
	note = models.TextField(blank=False, null=False)
	amount = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)

	class Meta:
		verbose_name_plural = "Invoice Completed"

	def __str__(self):
		return self.customer + " " + self.dispatch_number

class RelyPaid(models.Model):
	dispatch_number = models.CharField(max_length=50, blank=True, null=True)
	status = models.ForeignKey(Status, null=True, blank=True, on_delete=models.SET_NULL)
	customer = models.CharField(max_length=50, blank=True, null=True)
	date_received = models.DateField(default=timezone.now)  # Date the invoice was received
	date_invoiced = models.DateField(default=timezone.now)  # Date the invoice was invoiced
	note = models.TextField(blank=False, null=False)
	amount = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)

	class Meta:
		verbose_name_plural = "Rely Paid"

	def __str__(self):
		return self.customer + " " + self.dispatch_number


class RelyProblem(models.Model):
	dispatch_number = models.CharField(max_length=50, blank=True, null=True)
	status = models.ForeignKey(Status, null=True, blank=True, on_delete=models.SET_NULL)
	customer = models.CharField(max_length=50, blank=True, null=True)
	date_received = models.DateField(default=timezone.now)  # Date the invoice was received
	date_invoiced = models.DateField(default=timezone.now)  # Date the invoice was invoiced
	note = models.TextField(blank=False, null=False)
	amount = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)

	class Meta:
		verbose_name_plural = "Rely Problem"

	def __str__(self):
		return self.customer + " " + self.dispatch_number


class RelyReassigned(models.Model):
	dispatch_number = models.CharField(max_length=50, blank=True, null=True)
	status = models.ForeignKey(Status, null=True, blank=True, on_delete=models.SET_NULL)
	customer = models.CharField(max_length=50, blank=True, null=True)
	date_received = models.DateField(default=timezone.now)  # Date the invoice was received
	date_invoiced = models.DateField(default=timezone.now)  # Date the invoice was invoiced
	note = models.TextField(blank=False, null=False)
	amount = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)

	class Meta:
		verbose_name_plural = "Rely Reassigned"

	def __str__(self):
		return self.customer + " " + self.dispatch_number

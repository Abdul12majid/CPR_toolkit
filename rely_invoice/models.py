from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum

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
	date_paid = models.DateField(default=timezone.now)


	def __str__(self):
		return self.customer + " " + self.dispatch_number

	@property
	def days_difference(self):
		"""
        Calculate the difference in days between the current date and date_received.
        Returns None if date_received is missing or if amount is 0.
        """
		if self.date_received:
			current_date = timezone.now().date()
			difference = (current_date - self.date_received).days
			# If difference is 0, set it to 1
			return 1 if difference == 0 else difference
		return None

class RelyProcessed(models.Model):
    dispatch_number = models.CharField(max_length=50, blank=True, null=True)
    status = models.ForeignKey('Status', null=True, blank=True, on_delete=models.SET_NULL)
    customer = models.CharField(max_length=50, blank=True, null=True)
    date_received = models.DateField(default=timezone.now) 
    date_invoiced = models.DateField(default=timezone.now)
    note = models.TextField(blank=False, null=False)
    amount = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    date_paid = models.DateField(default=timezone.now)


    class Meta:
        verbose_name_plural = "RelyProcessed"

    def __str__(self):
        return f"{self.customer} {self.dispatch_number}"

    @property
    def due_days(self):
        """
        Calculate the difference in days between the current date and date_invoiced.
        Returns None if date_invoiced is missing or if amount is 0.
        """
        if self.date_invoiced:
            current_date = timezone.now().date()
            difference = (current_date - self.date_invoiced).days
            # If difference is 0, set it to 1
            return 1 if difference == 0 else difference
        return None

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
	date_paid = models.DateField(default=timezone.now)


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
	date_paid = models.DateField(default=timezone.now)


	class Meta:
		verbose_name_plural = "Rely Paid"

	def __str__(self):
		return self.customer + " " + self.dispatch_number

	@property
	def days_difference(self):
		"""
        Calculate the difference in days between the current date and date_invoiced.
        Returns None if date_invoiced is missing or if amount is 0.
        """
		if self.date_invoiced:
			current_date = timezone.now().date()
			difference = (current_date - self.date_invoiced).days
			# If difference is 0, set it to 1
			return 1 if difference == 0 else difference
		return None

class RelyProblem(models.Model):
	dispatch_number = models.CharField(max_length=50, blank=True, null=True)
	status = models.ForeignKey(Status, null=True, blank=True, on_delete=models.SET_NULL)
	customer = models.CharField(max_length=50, blank=True, null=True)
	date_received = models.DateField(default=timezone.now)  # Date the invoice was received
	date_invoiced = models.DateField(default=timezone.now)  # Date the invoice was invoiced
	note = models.TextField(blank=False, null=False)
	amount = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
	date_paid = models.DateField(default=timezone.now)


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
    date_paid = models.DateField(default=timezone.now)


    class Meta:
        verbose_name_plural = "Rely Reassigned"

    def __str__(self):
        return self.customer + " " + self.dispatch_number

    @classmethod
    def get_total_amount(cls):
        """
        Calculate the total amount of all RelyReassigned instances.
        """
        total = cls.objects.aggregate(total_amount=Sum('amount'))['total_amount']
        return total if total is not None else 0


class RelyGMMM(models.Model):
    dispatch_number = models.CharField(max_length=50, blank=True, null=True)
    status = models.ForeignKey(Status, null=True, blank=True, on_delete=models.SET_NULL)
    customer = models.CharField(max_length=50, blank=True, null=True)
    date_received = models.DateField(default=timezone.now)  # Date the invoice was received
    date_invoiced = models.DateField(default=timezone.now)  # Date the invoice was invoiced
    note = models.TextField(blank=False, null=False)
    amount = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    date_paid = models.DateField(default=timezone.now)


    class Meta:
        verbose_name_plural = "Rely GMMM"

    def __str__(self):
        return self.customer + " " + self.dispatch_number

    @classmethod
    def get_total_amount(cls):
        """
        Calculate the total amount of all RelyReassigned instances.
        """
        total = cls.objects.aggregate(total_amount=Sum('amount'))['total_amount']
        return total if total is not None else 0
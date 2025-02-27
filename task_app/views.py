from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .models import Task, Journal, Invoice
from .models import Belle_Task, Marvin_Task
from django.contrib import messages
from django.utils.timezone import now
from datetime import timedelta
from django.db.models import Sum, Avg
from django.core.paginator import Paginator
import pytz

# Create your views here.
def index(request):
	all_task = Task.objects.filter(status=False).order_by('-id')
	belle_task = Belle_Task.objects.filter(status=False).order_by('-id')
	marvin_task = Marvin_Task.objects.filter(status=False).order_by('-id')
	pst_tz = pytz.timezone("America/Los_Angeles")
	today = now().astimezone(pst_tz)
	print(today, flush=True)
	current_day = today
	seven_days_ago = today - timedelta(days=7)
	thirty_days_ago = today - timedelta(days=30)
	six_months_ago = today - timedelta(days=180)
	twelve_months_ago = today - timedelta(days=365)

	# Function to calculate average and total for a given queryset
	def get_avg_total(queryset):
		total = queryset.aggregate(total=Sum('invoiced_amount'))['total'] or 0
		avg = queryset.aggregate(avg=Avg('invoiced_amount'))['avg'] or 0
		return round(avg, 2), round(total, 2)
	# Filter invoices excluding those with 0$ amount
	current_day_avg, current_day_total = get_avg_total(
		Invoice.objects.filter(created_at__gte=current_day).exclude(invoiced_amount=0)
    )
	seven_day_avg, seven_day_total = get_avg_total(
		Invoice.objects.filter(created_at__gte=seven_days_ago).exclude(invoiced_amount=0)
    )
	thirty_day_avg, thirty_day_total = get_avg_total(
		Invoice.objects.filter(created_at__gte=thirty_days_ago).exclude(invoiced_amount=0)
    )
	six_month_avg, six_month_total = get_avg_total(
		Invoice.objects.filter(created_at__gte=six_months_ago).exclude(invoiced_amount=0)
    )
	twelve_month_avg, twelve_month_total = get_avg_total(
		Invoice.objects.filter(created_at__gte=twelve_months_ago).exclude(invoiced_amount=0)
    )
	# Calculate overall total
	overall_total = Invoice.objects.aggregate(total=Sum('invoiced_amount'))['total'] or 0
	overall_total = round(overall_total, 2)
	context = {
		"all_task":all_task,
		"belle_task":belle_task,
		"marvin_task":marvin_task,
		"current_day_avg": current_day_avg,
        "current_day_total": current_day_total,
        "seven_day_avg": seven_day_avg,
        "seven_day_total": seven_day_total,
        "thirty_day_avg": thirty_day_avg,
        "thirty_day_total": thirty_day_total,
        "six_month_avg": six_month_avg,
        "six_month_total": six_month_total,
        "twelve_month_avg": twelve_month_avg,
        "twelve_month_total": twelve_month_total,
        "overall_total": overall_total,
	}
	return render(request, "dashboard.html", context)


def add_task(request):
	if request.method == "POST":		
		description = request.POST['description']
		task = Task.objects.create(description=description)
		task.save()
		print("task created", flush=True)
		messages.success(request, ("Task Added for Bojan"))
		return redirect('index')
	return render(request, 'add_task.html')

def belle_task(request):
	if request.method == "POST":		
		description = request.POST['description']
		task = Belle_Task.objects.create(description=description)
		task.save()
		print("task created", flush=True)
		messages.success(request, ("Task Added for Belle"))
		return redirect('index')
	return render(request, 'add_task.html')

def marvin_task(request):
	if request.method == "POST":		
		description = request.POST['description']
		task = Marvin_Task.objects.create(description=description)
		task.save()
		print("task created", flush=True)
		messages.success(request, ("Task Added for Marvin"))
		return redirect('index')
	return render(request, 'add_task.html')

def update_task(request, pk):
	task = Task.objects.get(id=pk)
	context = {
		"task":task,
	}
	if request.method == "POST":	
		description = request.POST['description']
		task.description = description
		task.save()
		print("task Updated", flush=True)
		messages.success(request, ("Task updated"))
		return redirect('index')
	return render(request, 'update_task.html', context)

def update_belle_task(request, pk):
	task = Belle_Task.objects.get(id=pk)
	context = {
		"task":task,
	}
	if request.method == "POST":	
		description = request.POST['description']
		task.description = description
		task.save()
		print("task Updated", flush=True)
		messages.success(request, ("Task updated"))
		return redirect('index')
	return render(request, 'update_task.html', context)

def update_marvin_task(request, pk):
	task = Marvin_Task.objects.get(id=pk)
	context = {
		"task":task,
	}
	if request.method == "POST":	
		description = request.POST['description']
		task.description = description
		task.save()
		print("task Updated", flush=True)
		messages.success(request, ("Task updated"))
		return redirect('index')
	return render(request, 'update_task.html', context)

def complete_task(request, pk):
	task = Task.objects.get(id=pk)
	task.status = True
	task.save()
	messages.success(request, ("Task completed"))
	return redirect('index')

def complete_belle_task(request, pk):
	task = Belle_Task.objects.get(id=pk)
	task.status = True
	task.save()
	messages.success(request, ("Task completed"))
	return redirect('index')

def complete_marvin_task(request, pk):
	task = Marvin_Task.objects.get(id=pk)
	task.status = True
	task.save()
	messages.success(request, ("Task completed"))
	return redirect('index')


def thread(request):
	get_user = request.user
	all_threads = Journal.objects.all().order_by("-id")
	context = {
	"all_threads":all_threads,
	"get_user":get_user,
	}
	return render(request, 'thread.html', context)


def invoices(request):
    all_invoices = Invoice.objects.all().order_by("-id")
    search_results = None
    
    # Set PST timezone
    pst_tz = pytz.timezone("America/Los_Angeles")
    today = now().astimezone(pst_tz)
    
    print(today, flush=True)
    
    current_day = today
    seven_days_ago = today - timedelta(days=7)
    thirty_days_ago = today - timedelta(days=30)
    six_months_ago = today - timedelta(days=180)
    twelve_months_ago = today - timedelta(days=365)

    # Function to calculate average and total for a given queryset
    def get_avg_total(queryset):
        total = queryset.aggregate(total=Sum('invoiced_amount'))['total'] or 0
        avg = queryset.aggregate(avg=Avg('invoiced_amount'))['avg'] or 0
        return round(avg, 2), round(total, 2)

    # Filter invoices excluding those with 0$ amount
    current_day_avg, current_day_total = get_avg_total(
        Invoice.objects.filter(created_at__gte=current_day).exclude(invoiced_amount=0)
    )
    seven_day_avg, seven_day_total = get_avg_total(
        Invoice.objects.filter(created_at__gte=seven_days_ago).exclude(invoiced_amount=0)
    )
    thirty_day_avg, thirty_day_total = get_avg_total(
        Invoice.objects.filter(created_at__gte=thirty_days_ago).exclude(invoiced_amount=0)
    )
    six_month_avg, six_month_total = get_avg_total(
        Invoice.objects.filter(created_at__gte=six_months_ago).exclude(invoiced_amount=0)
    )
    twelve_month_avg, twelve_month_total = get_avg_total(
        Invoice.objects.filter(created_at__gte=twelve_months_ago).exclude(invoiced_amount=0)
    )

    # Calculate overall total
    overall_total = Invoice.objects.aggregate(total=Sum('invoiced_amount'))['total'] or 0
    overall_total = round(overall_total, 2)

    # Paginate invoices
    paginate = Paginator(all_invoices, 10)
    page = request.GET.get('page')
    invoices = paginate.get_page(page)

    # Handle search functionality
    if request.method == "POST":
        inv_data = request.POST.get('inv_data', '').strip()
        messages.success(request, f"You searched {inv_data}")
        
        if inv_data:
            search_results = Invoice.objects.filter(dispatch_no__icontains=inv_data) | \
                             Invoice.objects.filter(name__icontains=inv_data) | \
                             Invoice.objects.filter(invoiced_amount__icontains=inv_data)

    context = {
        "all_invoices": all_invoices,
        "search_results": search_results,
        "current_day_avg": current_day_avg,
        "current_day_total": current_day_total,
        "seven_day_avg": seven_day_avg,
        "seven_day_total": seven_day_total,
        "thirty_day_avg": thirty_day_avg,
        "thirty_day_total": thirty_day_total,
        "six_month_avg": six_month_avg,
        "six_month_total": six_month_total,
        "twelve_month_avg": twelve_month_avg,
        "twelve_month_total": twelve_month_total,
        "overall_total": overall_total,
        "invoices": invoices,
    }
    
    return render(request, "invoices.html", context)



def create_invoice(request):
	context = {
		"today_date": now().strftime("%Y-%m-%d")
		}
	if request.method == "POST":
		dispatch_no = request.POST['dispatch_no']
		name = request.POST['name']
		invoiced_amount = request.POST["invoiced_amount"]
		date_added = request.POST["date_added"]
		date_received = request.POST["date_received"]
		if not date_added:
			date_added = now().date()
		invoice = Invoice.objects.create(
			dispatch_no=dispatch_no, 
			name=name, 
			invoiced_amount=invoiced_amount,
			created_at=date_added,
			date_received=date_received,
			)
		invoice.save()
		print("Invoice created", flush=True)
		messages.success(request, ("Invoice Added"))
		return redirect('invoices')
	return render(request, 'create_invoice.html', context)


def update_invoice(request, pk):
	get_invoice = Invoice.objects.get(id=pk)
	inv_id = get_invoice.id
	print(inv_id, flush=True)
	context = {
		"name":get_invoice.name,
		"dispatch_no":get_invoice.dispatch_no,
		"inv_amount":get_invoice.invoiced_amount,
		'date_added':get_invoice.created_at,
		'date_received':get_invoice.date_received,
		"inv_id":inv_id,
	}
	print(get_invoice.created_at, flush=True)
	if request.method=="POST":
		dispatch_no = request.POST.get('dispatch_no')
		name = request.POST.get('name')
		inv_amount = request.POST.get('invoiced_amount')
		date_added = request.POST.get('date_added')
		date_received = request.POST.get('date_received')
		get_invoice.dispatch_no = dispatch_no
		get_invoice.name = name
		get_invoice.invoiced_amount = inv_amount
		get_invoice.created_at = date_added
		get_invoice.date_received = date_received
		get_invoice.save()
		messages.success(request, ("Invoice updated."))
		return redirect('invoices')
	return render(request, 'update_invoice.html', context)


def delete_invoice(request, pk):
    invoice = get_object_or_404(Invoice, id=pk)
    invoice.delete()
    messages.success(request, "Invoice deleted successfully.")
    return redirect("invoices")
    
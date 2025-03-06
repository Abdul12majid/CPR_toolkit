from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .models import Task, Journal, Invoice
from .models import Belle_Task, Marvin_Task
from django.contrib import messages
from django.utils.timezone import now
from datetime import timedelta
from django.db.models import Sum, Avg, F
from django.core.paginator import Paginator
import pytz
from django.utils import timezone
from django.utils.timezone import localtime
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.utils.timezone import make_aware, datetime

# Create your views here.
@login_required(login_url='login')
def index(request):
	all_task = Task.objects.filter(status=False).order_by('-id')
	belle_task = Belle_Task.objects.filter(status=False).order_by('-id')
	marvin_task = Marvin_Task.objects.filter(status=False).order_by('-id')
	pst_tz = pytz.timezone("America/Los_Angeles")
	now_pst = now().astimezone(pst_tz)
	today = now_pst.replace(hour=0, minute=0, second=0, microsecond=0)
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


@login_required(login_url='login')
def add_task(request):
	if request.method == "POST":		
		description = request.POST['description']
		task = Task.objects.create(description=description)
		task.save()
		print("task created", flush=True)
		messages.success(request, ("Task Added for Bojan"))
		return redirect('index')
	return render(request, 'add_task.html')

@login_required(login_url='login')
def belle_task(request):
	if request.method == "POST":		
		description = request.POST['description']
		task = Belle_Task.objects.create(description=description)
		task.save()
		print("task created", flush=True)
		messages.success(request, ("Task Added for Belle"))
		return redirect('index')
	return render(request, 'add_task.html')

@login_required(login_url='login')
def marvin_task(request):
	if request.method == "POST":		
		description = request.POST['description']
		task = Marvin_Task.objects.create(description=description)
		task.save()
		print("task created", flush=True)
		messages.success(request, ("Task Added for Marvin"))
		return redirect('index')
	return render(request, 'add_task.html')

@login_required(login_url='login')
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

@login_required(login_url='login')
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

@login_required(login_url='login')
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

@login_required(login_url='login')
def complete_task(request, pk):
	task = Task.objects.get(id=pk)
	task.status = True
	task.save()
	messages.success(request, ("Task completed"))
	return redirect('index')

@login_required(login_url='login')
def complete_belle_task(request, pk):
	task = Belle_Task.objects.get(id=pk)
	task.status = True
	task.save()
	messages.success(request, ("Task completed"))
	return redirect('index')

@login_required(login_url='login')
def complete_marvin_task(request, pk):
	task = Marvin_Task.objects.get(id=pk)
	task.status = True
	task.save()
	messages.success(request, ("Task completed"))
	return redirect('index')

@login_required(login_url='login')
def thread(request):
    get_user = request.user
    pst_tz = pytz.timezone("America/Los_Angeles")
    all_threads = Journal.objects.order_by("-id")[:10]
    
    for thread in all_threads:
        if thread.date_created.tzinfo is None:
            thread.date_created = pytz.utc.localize(thread.date_created)
        thread.date_created = thread.date_created.astimezone(pst_tz)
        print(f"Converted date: {thread.date_created}")  # Debugging output
    
    context = {
        "all_threads": all_threads,
        "get_user": get_user,
    }
    return render(request, "thread.html", context)

@login_required(login_url='login')
def invoices(request):
    all_invoices = Invoice.objects.all().order_by("-id")
    search_results = None
    
    # Set PST timezone
    pst_tz = pytz.timezone("America/Los_Angeles")
    
    # Get the current time in PST
    now_pst = timezone.now().astimezone(pst_tz)
    
    # Set today to the start of the day (00:00:00) in PST
    today = now_pst.replace(hour=0, minute=0, second=0, microsecond=0)
    
    print(f"Today: {today}", flush=True) 
    
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

    # Calculate average days to invoice for each period
    current_day_avg_days = Invoice.objects.filter(
        created_at__gte=current_day
    ).exclude(
        invoiced_amount=0
    ).exclude(
        created_at=F('date_received')  # Exclude invoices where created_at == date_received
    ).aggregate(
        avg_days=Avg(F('created_at') - F('date_received'))
    )['avg_days'] or timedelta(0)
    current_day_avg_days = current_day_avg_days.days  # Extract days

    seven_day_avg_days = Invoice.objects.filter(
        created_at__gte=seven_days_ago
    ).exclude(
        invoiced_amount=0
    ).exclude(
        created_at=F('date_received')  # Exclude invoices where created_at == date_received
    ).aggregate(
        avg_days=Avg(F('created_at') - F('date_received'))
    )['avg_days'] or timedelta(0)
    seven_day_avg_days = seven_day_avg_days.days  # Extract days

    thirty_day_avg_days = Invoice.objects.filter(
        created_at__gte=thirty_days_ago
    ).exclude(
        invoiced_amount=0
    ).exclude(
        created_at=F('date_received')  # Exclude invoices where created_at == date_received
    ).aggregate(
        avg_days=Avg(F('created_at') - F('date_received'))
    )['avg_days'] or timedelta(0)
    thirty_day_avg_days = thirty_day_avg_days.days  # Extract days

    six_month_avg_days = Invoice.objects.filter(
        created_at__gte=six_months_ago
    ).exclude(
        invoiced_amount=0
    ).exclude(
        created_at=F('date_received')  # Exclude invoices where created_at == date_received
    ).aggregate(
        avg_days=Avg(F('created_at') - F('date_received'))
    )['avg_days'] or timedelta(0)
    six_month_avg_days = six_month_avg_days.days  # Extract days

    twelve_month_avg_days = Invoice.objects.filter(
        created_at__gte=twelve_months_ago
    ).exclude(
        invoiced_amount=0
    ).exclude(
        created_at=F('date_received')  # Exclude invoices where created_at == date_received
    ).aggregate(
        avg_days=Avg(F('created_at') - F('date_received'))
    )['avg_days'] or timedelta(0)
    twelve_month_avg_days = twelve_month_avg_days.days  # Extract days

    overall_avg_days = Invoice.objects.exclude(
        invoiced_amount=0
    ).exclude(
        created_at=F('date_received')  # Exclude invoices where created_at == date_received
    ).aggregate(
        avg_days=Avg(F('created_at') - F('date_received'))
    )['avg_days'] or timedelta(0)
    overall_avg_days = overall_avg_days.days  # Extract days

    # Paginate invoices
    paginate = Paginator(all_invoices, 15)
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
        "current_day_avg_days": current_day_avg_days,
        "seven_day_avg_days": seven_day_avg_days,
        "thirty_day_avg_days": thirty_day_avg_days,
        "six_month_avg_days": six_month_avg_days,
        "twelve_month_avg_days": twelve_month_avg_days,
        "overall_avg_days": overall_avg_days,
    }
    
    return render(request, "AHS_invoices.html", context)

@login_required(login_url='login')
def create_invoice(request):
    pst_tz = pytz.timezone("America/Los_Angeles")
    today = timezone.now().astimezone(pst_tz)
    context = {
        "today_date": today.strftime("%Y-%m-%d")
    }

    if request.method == "POST":
        dispatch_no = request.POST.get('dispatch_no')
        name = request.POST.get('name')
        invoiced_amount_str = request.POST.get('invoiced_amount')
        invoiced_amount = float(invoiced_amount_str)
        date_added_str = request.POST.get('date_added')
        date_received_str = request.POST.get('date_received')

        # Validate required fields
        if not dispatch_no or not name:
            messages.success(request, "Dispatch No, Name, and Invoiced Amount are required.")
            return render(request, 'create_invoice.html', context)

        # Convert date strings to date objects
        try:
            date_added = datetime.strptime(date_added_str, "%Y-%m-%d").date() if date_added_str else today.date()
            date_received = datetime.strptime(date_received_str, "%Y-%m-%d").date() if date_received_str else today.date()
        except ValueError:
            messages.success(request, "Invalid date format. Please use YYYY-MM-DD.")
            return render(request, 'create_invoice.html', context)

        # Create and save the invoice
        invoice = Invoice(
            dispatch_no=dispatch_no,
            name=name,
            invoiced_amount=invoiced_amount,
            created_at=date_added,
            date_received=date_received,
        )
        invoice.save()

        print("Invoice created", flush=True)
        messages.success(request, "Invoice Added")
        return redirect('invoices')

    return render(request, 'create_invoice.html', context)


@login_required(login_url='login')
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
		date_added_str = request.POST.get('date_added')
		date_received_str = request.POST.get('date_received')
		date_added = datetime.strptime(date_added_str, "%Y-%m-%d").date() if date_added_str else today.date()
		date_received = datetime.strptime(date_received_str, "%Y-%m-%d").date() if date_received_str else today.date()
		get_invoice.dispatch_no = dispatch_no
		get_invoice.name = name
		get_invoice.invoiced_amount = int(inv_amount)
		get_invoice.created_at = date_added
		get_invoice.date_received = date_received
		get_invoice.save()
		messages.success(request, ("Invoice updated."))
		return redirect('invoices')
	return render(request, 'update_invoice.html', context)


@login_required(login_url='login')
def delete_invoice(request, pk):
    invoice = get_object_or_404(Invoice, id=pk)
    invoice.delete()
    messages.success(request, "Invoice deleted successfully.")
    return redirect("invoices")
    
@login_required(login_url='login')
def add_journal(request):
	if request.method == "POST":		
		description = request.POST['description']
		journal = Journal.objects.create(notes=description)
		journal.save()
		print("Journal Added created", flush=True)
		messages.success(request, ("Journal Created"))
		return redirect('journal')
	return render(request, 'add_journal.html')

def login_user(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			messages.success(request, ("Login Successful"))
			return redirect('index')
		else:
			messages.success(request, ("Invalid Login Details"))
			return redirect(request.META.get("HTTP_REFERER"))
	return render(request, "login.html")

def logout_user(request):
	logout(request)
	messages.success(request, ("You have logged out."))
	return redirect('login')

def test_page(request):
	return render(request, "test_page.html")

def delete_journal(request, pk):
    journal = get_object_or_404(Journal, pk=pk)
    journal.delete()
    messages.success(request, "Journal entry deleted successfully.")
    return redirect('journal')

def robots_txt(request):
    content = [
        "User-agent: *",
        "Disallow: /",
    ]
    return HttpResponse("\n".join(content), content_type="text/plain")

@login_required(login_url='login')
def update_journal(request, pk):
	journal = Journal.objects.get(id=pk)
	context = {
		"journal":journal,
	}
	if request.method == "POST":	
		j_note = request.POST['notes']
		journal.notes = j_note
		journal.save()
		print("Journal Updated", flush=True)
		messages.success(request, ("Journal updated"))
		return redirect('journal')
	return render(request, 'update_journal.html', context)
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .models import Task, Journal, Invoice, Ebay, Merchant, Work_Journal
from .models import Belle_Task, Marvin_Task, Today_order, Amex, us_bank
from rely_invoice.models import Work_Order, RelyProcessed, RelyGMMM, RelyReassigned
from rely_invoice.models import Status, RelyPaid, RelyProcessed
from django.contrib import messages
from django.utils.timezone import now
from datetime import timedelta
from django.db.models import Sum, Avg, F, Count, FloatField
from django.core.paginator import Paginator
import pytz
from django.utils import timezone
from django.utils.timezone import localtime
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.utils.timezone import make_aware, datetime
from django.db.models import Sum
from .push_over import belle_push_notis
from django.db.models.functions import Cast 
from django.db import models

# Create your views here.
@login_required(login_url='login')
def index(request):
    user = request.user
    if user.username == "Sergio" or user.username == "Sam":
        return redirect("payment_home")
    # Task-related data
    all_task = Task.objects.filter(status=False).order_by('-id')
    belle_task = Belle_Task.objects.filter(status=False).order_by('-id')
    marvin_task = Marvin_Task.objects.filter(status=False).order_by('-id')
    
    # Rely data
    all_rely_paid = RelyPaid.objects.all().order_by('-id')
    all_rely_processed = RelyProcessed.objects.all().order_by('-date_invoiced')
    all_statuses = Status.objects.all()

    # Set up timezone and date ranges 
    pst_tz = pytz.timezone("America/Los_Angeles")
    now_pst = timezone.now().astimezone(pst_tz)
    today = now_pst.replace(hour=0, minute=0, second=0, microsecond=0)
    current_day = today
    seven_days_ago = today - timedelta(days=7)
    thirty_days_ago = today - timedelta(days=30)
    six_months_ago = today - timedelta(days=180)
    twelve_months_ago = today - timedelta(days=365)

    # Current year calculations for RelyPaid
    current_year_start = datetime(now_pst.year, 1, 1).astimezone(pst_tz)
    current_year_total = RelyPaid.objects.filter(
        date_paid__gte=current_year_start,
        date_paid__lte=today
    ).aggregate(total=Sum('amount'))['total'] or 0

    # Last year calculations for RelyPaid
    last_year_start = datetime(now_pst.year - 1, 1, 1).astimezone(pst_tz)
    last_year_end = datetime(now_pst.year - 1, 12, 31).astimezone(pst_tz)
    last_year_total = RelyPaid.objects.filter(
        date_paid__gte=last_year_start,
        date_paid__lte=last_year_end
    ).aggregate(total=Sum('amount'))['total'] or 0

    # Helper function to calculate average and total amounts
    def get_avg_total(queryset, amount_field='amount'):
        total = queryset.aggregate(total=Sum(amount_field))['total'] or 0
        avg = queryset.aggregate(avg=Avg(amount_field))['avg'] or 0
        return round(avg, 2), round(total, 2)

    # Calculate average and total amounts for different time ranges (Invoice)
    current_day_avg, current_day_total = get_avg_total(
        Invoice.objects.filter(created_at__gte=current_day).exclude(invoiced_amount=0),
        'invoiced_amount'
    )
    seven_day_avg, seven_day_total = get_avg_total(
        Invoice.objects.filter(created_at__gte=seven_days_ago).exclude(invoiced_amount=0),
        'invoiced_amount'
    )
    thirty_day_avg, thirty_day_total = get_avg_total(
        Invoice.objects.filter(created_at__gte=thirty_days_ago).exclude(invoiced_amount=0),
        'invoiced_amount'
    )
    six_month_avg, six_month_total = get_avg_total(
        Invoice.objects.filter(created_at__gte=six_months_ago).exclude(invoiced_amount=0),
        'invoiced_amount'
    )
    twelve_month_avg, twelve_month_total = get_avg_total(
        Invoice.objects.filter(created_at__gte=twelve_months_ago).exclude(invoiced_amount=0),
        'invoiced_amount'
    )

    # Calculate average and total amounts for RelyPaid
    rely_paid_current_day_avg, rely_paid_current_day_total = get_avg_total(
        RelyPaid.objects.filter(date_paid__gte=current_day).exclude(amount=0)
    )
    rely_paid_seven_day_avg, rely_paid_seven_day_total = get_avg_total(
        RelyPaid.objects.filter(date_paid__gte=seven_days_ago).exclude(amount=0)
    )
    rely_paid_thirty_day_avg, rely_paid_thirty_day_total = get_avg_total(
        RelyPaid.objects.filter(date_paid__gte=thirty_days_ago).exclude(amount=0)
    )
    rely_paid_six_month_avg, rely_paid_six_month_total = get_avg_total(
        RelyPaid.objects.filter(date_paid__gte=six_months_ago).exclude(amount=0)
    )
    rely_paid_twelve_month_avg, rely_paid_twelve_month_total = get_avg_total(
        RelyPaid.objects.filter(date_paid__gte=twelve_months_ago).exclude(amount=0)
    )

    # Calculate average and total amounts for RelyProcessed
    rely_proc_current_day_avg, rely_proc_current_day_total = get_avg_total(
        RelyProcessed.objects.filter(date_invoiced__gte=current_day).exclude(amount=0)
    )
    rely_proc_seven_day_avg, rely_proc_seven_day_total = get_avg_total(
        RelyProcessed.objects.filter(date_invoiced__gte=seven_days_ago).exclude(amount=0)
    )
    rely_proc_thirty_day_avg, rely_proc_thirty_day_total = get_avg_total(
        RelyProcessed.objects.filter(date_invoiced__gte=thirty_days_ago).exclude(amount=0)
    )
    rely_proc_six_month_avg, rely_proc_six_month_total = get_avg_total(
        RelyProcessed.objects.filter(date_invoiced__gte=six_months_ago).exclude(amount=0)
    )
    rely_proc_twelve_month_avg, rely_proc_twelve_month_total = get_avg_total(
        RelyProcessed.objects.filter(date_invoiced__gte=twelve_months_ago).exclude(amount=0)
    )

    # Helper function to calculate average days difference for RelyProcessed
    def get_avg_days(queryset):
        total_days = 0
        count = 0
        for invoice in queryset:
            if invoice.date_invoiced and invoice.date_received:
                days_diff = (invoice.date_invoiced - invoice.date_received).days
                if days_diff != 0:  # Exclude cases where date_invoiced == date_received
                    total_days += days_diff
                    count += 1
        return round(total_days / count, 2) if count > 0 else 0

    # Helper function to calculate average due_days for RelyProcessed
    def get_avg_due_days(queryset):
        total_due_days = 0
        count = 0
        for invoice in queryset:
            if invoice.due_days is not None:
                total_due_days += invoice.due_days
                count += 1
        return round(total_due_days / count, 2) if count > 0 else 0

    # Calculate average days difference for RelyProcessed
    current_day_avg_days = get_avg_days(
        RelyProcessed.objects.filter(date_invoiced__gte=current_day).exclude(amount=0)
    )
    seven_day_avg_days = get_avg_days(
        RelyProcessed.objects.filter(date_invoiced__gte=seven_days_ago).exclude(amount=0)
    )
    thirty_day_avg_days = get_avg_days(
        RelyProcessed.objects.filter(date_invoiced__gte=thirty_days_ago).exclude(amount=0)
    )
    six_month_avg_days = get_avg_days(
        RelyProcessed.objects.filter(date_invoiced__gte=six_months_ago).exclude(amount=0)
    )
    twelve_month_avg_days = get_avg_days(
        RelyProcessed.objects.filter(date_invoiced__gte=twelve_months_ago).exclude(amount=0)
    )

    # Calculate average due_days for RelyProcessed
    current_day_avg_due_days = get_avg_due_days(
        RelyProcessed.objects.filter(date_invoiced__gte=current_day).exclude(amount=0)
    )
    seven_day_avg_due_days = get_avg_due_days(
        RelyProcessed.objects.filter(date_invoiced__gte=seven_days_ago).exclude(amount=0)
    )
    thirty_day_avg_due_days = get_avg_due_days(
        RelyProcessed.objects.filter(date_invoiced__gte=thirty_days_ago).exclude(amount=0)
    )
    six_month_avg_due_days = get_avg_due_days(
        RelyProcessed.objects.filter(date_invoiced__gte=six_months_ago).exclude(amount=0)
    )
    twelve_month_avg_due_days = get_avg_due_days(
        RelyProcessed.objects.filter(date_invoiced__gte=twelve_months_ago).exclude(amount=0)
    )

    # Calculate overall totals
    overall_total = Invoice.objects.aggregate(total=Sum('invoiced_amount'))['total'] or 0
    overall_total = round(overall_total, 2)
    
    overall_rely_paid_total = RelyPaid.objects.aggregate(total=Sum('amount'))['total'] or 0
    overall_rely_paid_total = round(overall_rely_paid_total, 2)
    
    overall_rely_proc_total = RelyProcessed.objects.aggregate(total=Sum('amount'))['total'] or 0
    overall_rely_proc_total = round(overall_rely_proc_total, 2)
    
    # Calculate overall averages for RelyProcessed
    overall_avg_days = get_avg_days(RelyProcessed.objects.exclude(amount=0))
    overall_avg_due_days = get_avg_due_days(RelyProcessed.objects.exclude(amount=0))

    # Rely reassigned and GMMM calculations
    total_amount = RelyReassigned.get_total_amount()
    total_gmmm_amount = RelyGMMM.get_total_amount()
    diff = total_amount - total_gmmm_amount
    check_str = str(overall_rely_proc_total)
    negative = "-" in check_str

    # Other dashboard data
    work_orders = Work_Order.objects.all().order_by('-id')[:10]
    work_journals = Work_Journal.objects.all().order_by('-id')[:12]

    # Pagination for Rely data
    paid_paginate = Paginator(all_rely_paid, 30)
    paid_page = request.GET.get('paid_page')
    rely_paid_invoices = paid_paginate.get_page(paid_page)

    proc_paginate = Paginator(all_rely_processed, 20)
    proc_page = request.GET.get('proc_page')
    rely_proc_invoices = proc_paginate.get_page(proc_page)

    
    context = {
        # Task data
        "all_task": all_task,
        "belle_task": belle_task,
        "marvin_task": marvin_task,
        
        # Invoice data
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
        
        # RelyPaid data
        "rely_paid_current_day_avg": rely_paid_current_day_avg,
        "rely_paid_current_day_total": rely_paid_current_day_total,
        "rely_paid_seven_day_avg": rely_paid_seven_day_avg,
        "rely_paid_seven_day_total": rely_paid_seven_day_total,
        "rely_paid_thirty_day_avg": rely_paid_thirty_day_avg,
        "rely_paid_thirty_day_total": rely_paid_thirty_day_total,
        "rely_paid_six_month_avg": rely_paid_six_month_avg,
        "rely_paid_six_month_total": rely_paid_six_month_total,
        "rely_paid_twelve_month_avg": rely_paid_twelve_month_avg,
        "rely_paid_twelve_month_total": rely_paid_twelve_month_total,
        "current_year_total": round(current_year_total, 2),
        "last_year_total": round(last_year_total, 2),
        "overall_rely_paid_total": overall_rely_paid_total,
        "all_rely_paid": all_rely_paid,
        "rely_paid_invoices": rely_paid_invoices,
        
        # RelyProcessed data
        "rely_proc_current_day_avg": rely_proc_current_day_avg,
        "rely_proc_current_day_total": rely_proc_current_day_total,
        "rely_proc_seven_day_avg": rely_proc_seven_day_avg,
        "rely_proc_seven_day_total": rely_proc_seven_day_total,
        "rely_proc_thirty_day_avg": rely_proc_thirty_day_avg,
        "rely_proc_thirty_day_total": rely_proc_thirty_day_total,
        "rely_proc_six_month_avg": rely_proc_six_month_avg,
        "rely_proc_six_month_total": rely_proc_six_month_total,
        "rely_proc_twelve_month_avg": rely_proc_twelve_month_avg,
        "rely_proc_twelve_month_total": rely_proc_twelve_month_total,
        "current_day_avg_days": current_day_avg_days,
        "seven_day_avg_days": seven_day_avg_days,
        "thirty_day_avg_days": thirty_day_avg_days,
        "six_month_avg_days": six_month_avg_days,
        "twelve_month_avg_days": twelve_month_avg_days,
        "current_day_avg_due_days": current_day_avg_due_days,
        "seven_day_avg_due_days": seven_day_avg_due_days,
        "thirty_day_avg_due_days": thirty_day_avg_due_days,
        "six_month_avg_due_days": six_month_avg_due_days,
        "twelve_month_avg_due_days": twelve_month_avg_due_days,
        "overall_avg_days": overall_avg_days,
        "overall_avg_due_days": overall_avg_due_days,
        "overall_rely_proc_total": overall_rely_proc_total,
        "all_rely_processed": all_rely_processed,
        "rely_proc_invoices": rely_proc_invoices,
        "all_statuses": all_statuses,
        
        # Other data
        "overall_rely_total": overall_rely_proc_total,  # Keeping for backward compatibility
        "diff": diff,
        "total_gmmm_amount": total_gmmm_amount,
        "negative": negative,
        "work_orders": work_orders,
        "work_journals": work_journals,
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
        words = description.split()[:5]  # Split into words and take first 5
        truncated_description = "BELLE: " + ' '.join(words) + '... ' if len(words) >= 5 else "BELLE: " + str(description)
        belle_push_notis(description)
        journal = Work_Journal.objects.create(description=truncated_description)
        journal.save()
        print("task created, notification sent", flush=True)
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
    
    # Truncate description to first 5 words + "..."
    words = task.description.split()[:25]  # Split into words and take first 25
    truncated_description = ' '.join(words) + '...' if len(words) >= 25 else task.description
    
    task.status = True
    task.save()
    
    # Save truncated description in Work_Journal
    journal = Journal.objects.create(notes=truncated_description)
    journal.save()
    
    messages.success(request, "Task completed")
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
    # Get all invoices ordered by most recent first
    all_invoices = Invoice.objects.all().order_by("-id")
    search_results = None
    
    # Set PST timezone
    pst_tz = pytz.timezone("America/Los_Angeles")
    
    # Get current time in PST
    now_pst = timezone.now().astimezone(pst_tz)
    
    # Define time periods
    today = now_pst.replace(hour=0, minute=0, second=0, microsecond=0)
    yesterday_start = today - timedelta(days=1)
    yesterday_end = today  # Midnight this morning
    current_day = today
    seven_days_ago = today - timedelta(days=7)
    thirty_days_ago = today - timedelta(days=30)
    six_months_ago = today - timedelta(days=180)
    twelve_months_ago = today - timedelta(days=365)
    ten_days_ago = today - timedelta(days=10)

    # Get old unpaid invoices
    old_invoices = Invoice.objects.filter(date_received__lt=ten_days_ago, invoiced_amount=0)

    # Helper functions
    def get_avg_total(queryset):
        """Returns (average, total) for non-zero invoices"""
        filtered = queryset.exclude(invoiced_amount=0)
        total = filtered.aggregate(total=Sum('invoiced_amount'))['total'] or 0
        avg = filtered.aggregate(avg=Avg('invoiced_amount'))['avg'] or 0
        return round(avg, 2), round(total, 2)

    def get_count(queryset):
        """Returns count of all invoices (including $0)"""
        return queryset.count()

    def get_avg_days(queryset):
        """Returns average days between date_received and created_at"""
        result = queryset.exclude(
            invoiced_amount=0
        ).exclude(
            created_at=F('date_received')
        ).aggregate(
            avg_days=Avg(F('created_at') - F('date_received'))
        )['avg_days'] or timedelta(0)
        return result.days if result else 0

    # Get stats for each time period
    ## Yesterday stats
    yesterday_queryset = Invoice.objects.filter(
        created_at__gte=yesterday_start,
        created_at__lt=yesterday_end
    )
    yesterday_count = get_count(yesterday_queryset)
    yesterday_avg, yesterday_total = get_avg_total(yesterday_queryset)
    yesterday_avg_days = get_avg_days(yesterday_queryset)
    
    ## Current day stats
    current_day_queryset = Invoice.objects.filter(created_at__gte=current_day)
    current_day_avg, current_day_total = get_avg_total(current_day_queryset)
    current_day_count = get_count(current_day_queryset)
    current_day_avg_days = get_avg_days(current_day_queryset)

    ## 7-day stats
    seven_day_queryset = Invoice.objects.filter(created_at__gte=seven_days_ago)
    seven_day_avg, seven_day_total = get_avg_total(seven_day_queryset)
    seven_day_count = get_count(seven_day_queryset)
    seven_day_avg_days = get_avg_days(seven_day_queryset)

    ## 30-day stats
    thirty_day_queryset = Invoice.objects.filter(created_at__gte=thirty_days_ago)
    thirty_day_avg, thirty_day_total = get_avg_total(thirty_day_queryset)
    thirty_day_count = get_count(thirty_day_queryset)
    thirty_day_avg_days = get_avg_days(thirty_day_queryset)

    ## 6-month stats
    six_month_queryset = Invoice.objects.filter(created_at__gte=six_months_ago)
    six_month_avg, six_month_total = get_avg_total(six_month_queryset)
    six_month_count = get_count(six_month_queryset)
    six_month_avg_days = get_avg_days(six_month_queryset)

    ## 12-month stats
    twelve_month_queryset = Invoice.objects.filter(created_at__gte=twelve_months_ago)
    twelve_month_avg, twelve_month_total = get_avg_total(twelve_month_queryset)
    twelve_month_count = get_count(twelve_month_queryset)
    twelve_month_avg_days = get_avg_days(twelve_month_queryset)

    ## Overall stats
    overall_total = round(Invoice.objects.exclude(invoiced_amount=0).aggregate(total=Sum('invoiced_amount'))['total'] or 0, 2)
    overall_count = get_count(Invoice.objects.all())
    overall_avg_days = get_avg_days(Invoice.objects.all())

    # Yearly stats
    current_year_start = datetime(now_pst.year, 1, 1).astimezone(pst_tz)
    current_year_total = round(Invoice.objects.filter(
        created_at__gte=current_year_start,
        created_at__lte=today
    ).exclude(invoiced_amount=0).aggregate(total=Sum('invoiced_amount'))['total'] or 0, 2)
    current_year_count = get_count(Invoice.objects.filter(
        created_at__gte=current_year_start,
        created_at__lte=today
    ))
    
    last_year_start = datetime(now_pst.year - 1, 1, 1).astimezone(pst_tz)
    last_year_end = datetime(now_pst.year - 1, 12, 31).astimezone(pst_tz)
    last_year_total = round(Invoice.objects.filter(
        created_at__gte=last_year_start,
        created_at__lte=last_year_end
    ).exclude(invoiced_amount=0).aggregate(total=Sum('invoiced_amount'))['total'] or 0, 2)
    last_year_count = get_count(Invoice.objects.filter(
        created_at__gte=last_year_start,
        created_at__lte=last_year_end
    ))

    # Pagination
    paginate = Paginator(all_invoices, 15)
    page = request.GET.get('page')
    invoices = paginate.get_page(page)

    # Search functionality
    if request.method == "POST":
        inv_data = request.POST.get('inv_data', '').strip()
        messages.success(request, f"You searched {inv_data}") 
        
        if inv_data:
            search_results = Invoice.objects.filter(dispatch_no__icontains=inv_data) | \
                           Invoice.objects.filter(name__icontains=inv_data) | \
                           Invoice.objects.filter(invoiced_amount__icontains=inv_data)

    # Prepare context
    context = {
        "all_invoices": all_invoices,
        "search_results": search_results,
        
        # Yesterday stats
        "yesterday_count": yesterday_count,
        "yesterday_avg": yesterday_avg,
        "yesterday_total": yesterday_total,
        "yesterday_avg_days": yesterday_avg_days,
        
        # Current day stats
        "current_day_avg": current_day_avg,
        "current_day_total": current_day_total,
        "current_day_count": current_day_count,
        "current_day_avg_days": current_day_avg_days,
        
        # 7-day stats
        "seven_day_avg": seven_day_avg,
        "seven_day_total": seven_day_total,
        "seven_day_count": seven_day_count,
        "seven_day_avg_days": seven_day_avg_days,
        
        # 30-day stats
        "thirty_day_avg": thirty_day_avg,
        "thirty_day_total": thirty_day_total,
        "thirty_day_count": thirty_day_count,
        "thirty_day_avg_days": thirty_day_avg_days,
        
        # 6-month stats
        "six_month_avg": six_month_avg,
        "six_month_total": six_month_total,
        "six_month_count": six_month_count,
        "six_month_avg_days": six_month_avg_days,
        
        # 12-month stats
        "twelve_month_avg": twelve_month_avg,
        "twelve_month_total": twelve_month_total,
        "twelve_month_count": twelve_month_count,
        "twelve_month_avg_days": twelve_month_avg_days,
        
        # Overall stats
        "overall_total": overall_total,
        "overall_count": overall_count,
        "overall_avg_days": overall_avg_days,
        
        # Yearly stats
        "current_year_total": current_year_total,
        "current_year_count": current_year_count,
        "last_year_total": last_year_total,
        "last_year_count": last_year_count,
        
        # Other data
        "invoices": invoices,
        "old_invoices": old_invoices,
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


@login_required(login_url='login')
def ebay(request):
    all_ebay = Ebay.objects.all().order_by("-id")[:30]
    pst_tz = pytz.timezone("America/Los_Angeles")
    now_pst = now().astimezone(pst_tz)
    today_pst = now_pst.date()
    print(today_pst, flush=True)
    today_order = Today_order.objects.filter(date_pushed=today_pst)
    search_results = None
    # Handle search functionality
    if request.method == "POST":
        ebay_data = request.POST.get('ebay_data', '').strip()
        messages.success(request, f"You searched {ebay_data}")
        
        if ebay_data:
            search_results = Ebay.objects.filter(name__icontains=ebay_data) | \
                             Ebay.objects.filter(tracking_number__icontains=ebay_data) | \
                             Ebay.objects.filter(order_number__icontains=ebay_data)
    context = {
        "all_ebay":all_ebay,
        'search_results':search_results,
        "today_order":today_order,
    }
    return render(request, 'ebay.html', context)

from datetime import date, timedelta
from itertools import chain
@login_required(login_url='login')
def merchant(request):
    user = request.user
    
    # Time setup (PST)
    pst = pytz.timezone("America/Los_Angeles")
    now_pst = timezone.now().astimezone(pst)
    today = now_pst.replace(hour=0, minute=0, second=0, microsecond=0)

    # Calculate time periods
    start_of_week = today - timedelta(days=today.weekday())
    start_of_month = today.replace(day=1)
    start_of_year = today.replace(month=1, day=1)
    start_of_last_year = start_of_year - timedelta(days=365)
    end_of_last_year = start_of_year - timedelta(days=1)

    def calculate_model_stats(model, date_field='date_pushed'):
        """Helper function to calculate statistics for a given model"""
        # Get all transactions with converted amounts
        transactions = model.objects.all().order_by("-id").annotate(
            amount_float=Cast('amount', FloatField())
        )

        # Calculate totals using the converted amount_float
        def get_total(queryset):
            return queryset.aggregate(total=Sum('amount_float'))['total'] or 0.0

        today_total = get_total(transactions.filter(**{f'{date_field}__gte': today}))
        week_total = get_total(transactions.filter(**{f'{date_field}__gte': start_of_week}))
        month_total = get_total(transactions.filter(**{f'{date_field}__gte': start_of_month}))
        year_total = get_total(transactions.filter(**{f'{date_field}__gte': start_of_year}))
        last_year_total = get_total(transactions.filter(
            **{f'{date_field}__gte': start_of_last_year,
               f'{date_field}__lte': end_of_last_year}
        ))

        # Calculate average per day
        avg_per_day = transactions.exclude(amount_float=0).aggregate(
            avg=Avg('amount_float')
        )['avg'] or 0.0

        # Calculate accurate average per month
        from django.db.models.functions import ExtractMonth, ExtractYear
        from calendar import monthrange

        # Get all unique month-year combinations
        month_years = transactions.annotate(
            month=ExtractMonth(date_field),
            year=ExtractYear(date_field)
        ).values('month', 'year').distinct()

        monthly_averages = []
        for my in month_years:
            year = my['year']
            month = my['month']
            
            # Get first and last day of month
            _, last_day = monthrange(year, month)
            start_date = date(year, month, 1)
            end_date = date(year, month, last_day)
            
            # Get transactions for this month
            month_trans = transactions.filter(
                **{f'{date_field}__gte': start_date,
                   f'{date_field}__lte': end_date}
            )
            
            # Calculate total for month and divide by days in month
            month_sum = get_total(month_trans)
            monthly_averages.append(month_sum / last_day)

        # Calculate overall monthly average
        avg_per_month = sum(monthly_averages) / len(monthly_averages) if monthly_averages else 0.0

        return {
            'today_total': today_total,
            'week_total': week_total,
            'month_total': month_total,
            'year_total': year_total,
            'last_year_total': last_year_total,
            'avg_per_day': avg_per_day,
            'avg_per_month': avg_per_month,
            'all_transactions': transactions,
        }

    # Calculate stats for both models
    merchant_stats = calculate_model_stats(Merchant)
    amex_stats = calculate_model_stats(Amex, date_field='date_pushed')  # Adjust if Amex uses different date field
    bank_data = us_bank.objects.all().order_by("-date_sent")
    month_start = today.replace(day=1)
    thirty_days_ago = today - timedelta(days=30)
    current_year = today.year
    last_year = current_year - 1
    year_start = today.replace(month=1, day=1)
    last_year_start = year_start.replace(year=last_year)
    last_year_end = year_start - timedelta(days=1)

    #today
    today_in = us_bank.objects.filter(
        date_sent=today,
        transaction_type__in=["Deposit"]
    ).aggregate(total=models.Sum('amount'))['total'] or 0
    
    today_out = us_bank.objects.filter(
        date_sent=today,
        transaction_type__in=["Withdrawn", "Zelle Payment"]
    ).aggregate(total=models.Sum('amount'))['total'] or 0

    # This month's transactions
    month_in = us_bank.objects.filter(
        date_sent__gte=month_start,
        transaction_type__in=["Deposit"]
    ).aggregate(total=models.Sum('amount'))['total'] or 0
    
    month_out = us_bank.objects.filter(
        date_sent__gte=month_start,
        transaction_type__in=["Withdrawn", "Zelle Payment"]
    ).aggregate(total=models.Sum('amount'))['total'] or 0

    # All-time transactions
    total_in = us_bank.objects.filter(
        transaction_type__in=["Deposit"]
    ).aggregate(total=models.Sum('amount'))['total'] or 0
    
    total_out = us_bank.objects.filter(
        transaction_type__in=["Withdrawn", "Zelle Payment"]
    ).aggregate(total=models.Sum('amount'))['total'] or 0

    # Last 30 days transactions
    last30_in = us_bank.objects.filter(
        date_sent__gte=thirty_days_ago,
        transaction_type__in=["Deposit"]
    ).aggregate(total=models.Sum('amount'))['total'] or 0


    #year in totals
    this_year_in = us_bank.objects.filter(
        date_sent__gte=year_start,
        transaction_type__in=["Deposit"]
    ).aggregate(total=models.Sum('amount'))['total'] or 0


    this_year_in_cd = us_bank.objects.filter(
        date_sent__gte=year_start,
        transaction_type__in=["Check Deposit"]
    ).aggregate(total=models.Sum('amount'))['total'] or 0

    print(f"This year in check deposit {this_year_in_cd}", flush=True)

    last_year_in = us_bank.objects.filter(
        date_sent__gte=last_year_start,
        date_sent__lte=last_year_end,
        transaction_type__in=["Deposit"]
    ).aggregate(total=models.Sum('amount'))['total'] or 0



    # Combined search functionality for both models
    search_results = None
    amex_search_results = None
    if request.method == "POST":
        query = request.POST.get('ebay_data', '').strip()
        if query:
            messages.success(request, f"You searched {query}")
            # Search both models
            m_search_results = Merchant.objects.filter(
                order_number__icontains=query
            ).annotate(amount_float=Cast('amount', FloatField()))
            
            amex_search_results = Amex.objects.filter(
                order_number__icontains=query
            ).annotate(amount_float=Cast('amount', FloatField()))
            
            # Combine the search results if needed
            search_results = list(m_search_results) + list(amex_search_results)

    # Combine stats with model prefixes
    combined_stats = {
        'today_total': merchant_stats['today_total'],
        'week_total': merchant_stats['week_total'],
        'month_total': merchant_stats['month_total'],
        'year_total': merchant_stats['year_total'],
        'last_year_total': merchant_stats['last_year_total'],
        'avg_per_day': merchant_stats['avg_per_day'],
        'avg_per_month': merchant_stats['avg_per_month'],
        'all_transactions': merchant_stats['all_transactions'],
        
        'amex_today_total': amex_stats['today_total'],
        'amex_week_total': amex_stats['week_total'],
        'amex_month_total': amex_stats['month_total'],
        'amex_year_total': amex_stats['year_total'],
        'amex_last_year_total': amex_stats['last_year_total'],
        'amex_avg_per_day': amex_stats['avg_per_day'],
        'amex_avg_per_month': amex_stats['avg_per_month'],
        'amex_all_transactions': amex_stats['all_transactions'],
        'search_results':search_results,

        "bank_data":bank_data,
        'today_in': today_in,
        'today_out': today_out,
        'month_in': month_in,
        'month_out': month_out,
        'total_in': total_in,
        'total_out': total_out,
        'last30_in': last30_in,
        'this_year_in': this_year_in,
        'last_year_in': last_year_in,
        
    }

    

    return render(request, 'merchant.html', combined_stats)
    

@login_required(login_url='login')
def create_ebay(request):
    if request.method == "POST":        
        name = request.POST['name']
        tracking_number = request.POST['tracking_number']
        order_number = request.POST['order_number']
        link = request.POST['link']
        delivery_time = request.POST['delivery_time']
        ebay = Ebay.objects.create(
            name=name, 
            tracking_number=tracking_number, 
            order_number=order_number,
            link=link,
            delivery_time=delivery_time
            )
        ebay.save()
        print("Data Added created", flush=True)
        messages.success(request, ("Data Added"))
        return redirect('ebay')
    return render(request, 'create_ebay.html')


def db_page(request):
    range_20 = range(1, 21)  # Just for the template loop
    context = {
        'range_20': range_20,
        
    }
    return render(request, 'db_page.html', context)
from django.shortcuts import render, HttpResponse, redirect
from .models import Task, Journal, Invoice
from django.contrib import messages
from django.utils.timezone import now
from datetime import timedelta
from django.db.models import Sum, Avg


# Create your views here.
def index(request):
	all_task = Task.objects.all().order_by('-id')
	context = {
		"all_task":all_task,
	}
	return render(request, "index.html", context)


def add_task(request):
	if request.method == "POST":
		name = request.POST['task_name']
		description = request.POST['description']
		task = Task.objects.create(name=name, description=description)
		task.save()
		print("task created", flush=True)
		messages.success(request, ("Task Added"))
		return redirect('index')
	return render(request, 'add_task.html')

def update_task(request, pk):
	task = Task.objects.get(id=pk)
	context = {
		"task":task,
	}
	if request.method == "POST":
		name = request.POST['task_name']
		description = request.POST['description']
		task.name = name
		task.description = description
		task.save()
		print("task Updated", flush=True)
		messages.success(request, ("Task updateed"))
		return redirect('index')
	return render(request, 'update_task.html', context)

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

    today = now()
    seven_days_ago = today - timedelta(days=7)
    thirty_days_ago = today - timedelta(days=30)
    six_months_ago = today - timedelta(days=180)
    twelve_months_ago = today - timedelta(days=365)

    
    def get_avg_total(queryset):
        total = queryset.aggregate(total=Sum('invoiced_amount'))['total'] or 0
        avg = queryset.aggregate(avg=Avg('invoiced_amount'))['avg'] or 0
        return round(avg, 2), round(total, 2)

    
    seven_day_avg, seven_day_total = get_avg_total(Invoice.objects.filter(created_at__gte=seven_days_ago))
    thirty_day_avg, thirty_day_total = get_avg_total(Invoice.objects.filter(created_at__gte=thirty_days_ago))
    six_month_avg, six_month_total = get_avg_total(Invoice.objects.filter(created_at__gte=six_months_ago))
    twelve_month_avg, twelve_month_total = get_avg_total(Invoice.objects.filter(created_at__gte=twelve_months_ago))
    overall_total = Invoice.objects.aggregate(total=Sum('invoiced_amount'))['total'] or 0
    overall_total = round(overall_total, 2)

    context = {
        "all_invoices": all_invoices,
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
    return render(request, "invoices.html", context)


def create_invoice(request):
	if request.method == "POST":
		dispatch_no = request.POST['dispatch_no']
		name = request.POST['name']
		invoiced_amount = request.POST["invoiced_amount"]
		invoice = Invoice.objects.create(dispatch_no=dispatch_no, name=name, invoiced_amount=invoiced_amount)
		invoice.save()
		print("Invoice created", flush=True)
		messages.success(request, ("Invoice Added"))
		return redirect('invoices')
	return render(request, 'create_invoice.html')
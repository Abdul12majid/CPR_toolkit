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
    total = Invoice.objects.aggregate(total=Sum('invoiced_amount'))['total'] or 0
    seven_day_avg = Invoice.objects.filter(
        created_at__gte=now() - timedelta(days=7)
    ).aggregate(avg=Avg('invoiced_amount'))['avg'] or 0
    thirty_day_avg = Invoice.objects.filter(
        created_at__gte=now() - timedelta(days=30)
    ).aggregate(avg=Avg('invoiced_amount'))['avg'] or 0

    context = {
        "all_invoices": all_invoices,
        "total": total,
        "seven_day_avg": seven_day_avg,
        "thirty_day_avg": thirty_day_avg,
    }
    return render(request, "invoices.html", context)

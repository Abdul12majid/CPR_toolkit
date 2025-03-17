from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .models import RelyInvoice, Status, RelyProcessed, RelyCompleted, RelyPaid, RelyProblem
from django.contrib import messages 
from django.contrib.auth.decorators import login_required
from django.utils.timezone import make_aware, datetime
from django.utils.timezone import now
import pytz

# Create your views here.
def rely_invoice(request):
    all_invoice = RelyInvoice.objects.all().order_by('-id')
    all_statuses = Status.objects.all()
    pst_tz = pytz.timezone("America/Los_Angeles")
    now_pst = now().astimezone(pst_tz)
    print(now_pst, flush=True)
    search_results = None
    if request.method == "POST":
        inv_data = request.POST.get('inv_data', '').strip()
        messages.success(request, f"You searched {inv_data}")
        
        if inv_data:
            search_results = RelyInvoice.objects.filter(dispatch_number__icontains=inv_data) | \
                             RelyInvoice.objects.filter(customer__icontains=inv_data)
    context = {
        "all_invoice": all_invoice,
        "all_statuses": all_statuses,
        'search_results':search_results
    }
    return render(request, 'rely_inv.html', context) 

@login_required(login_url='login')
def update_r_invoice(request, pk):
    get_invoice = RelyInvoice.objects.get(id=pk)
    inv_id = get_invoice.id
    print(inv_id, flush=True)
    context = {
        "customer":get_invoice.customer,
        "dispatch_no":get_invoice.dispatch_number,
        "inv_amount":get_invoice.amount,
        'date_invoiced':get_invoice.date_invoiced,
        'date_received':get_invoice.date_received,
        'note':get_invoice.note,
        "inv_id":inv_id,
    }
    print(get_invoice.date_invoiced, flush=True)
    if request.method=="POST":
        dispatch_no = request.POST.get('dispatch_no')
        customer = request.POST.get('name')
        inv_amount = request.POST.get('invoiced_amount')
        note = request.POST.get('note')
        date_added_str = request.POST.get('date_added')
        date_received_str = request.POST.get('date_received')
        date_added = datetime.strptime(date_added_str, "%Y-%m-%d").date() if date_added_str else today.date()
        date_received = datetime.strptime(date_received_str, "%Y-%m-%d").date() if date_received_str else today.date()
        get_invoice.dispatch_no = dispatch_no
        get_invoice.customer = customer
        get_invoice.note = note
        get_invoice.amount = int(inv_amount)
        get_invoice.date_invoiced = date_added
        get_invoice.date_received = date_received
        get_invoice.save()
        messages.success(request, ("Invoice updated."))
        #sending to invoice model
        invoiced = RelyProcessed.objects.create(
            dispatch_number = get_invoice.dispatch_number,
            status=get_invoice.status,
            customer=get_invoice.customer,
            date_received=get_invoice.date_received,
            note=get_invoice.note,
            amount=get_invoice.amount
        )
        invoiced.save()
        get_invoice.delete()
        return redirect('rely_invoice')
    return render(request, 'update_r_invoice.html', context)

@login_required(login_url='login')
def delete_r_invoice(request, pk):
    invoice = get_object_or_404(RelyInvoice, id=pk)
    invoice.delete()
    messages.success(request, ("Invoice Deleted."))
    return redirect("rely_invoice")

def invoice_status(request, pk):
    try:
        invoice = get_object_or_404(RelyInvoice, id=pk)
    except:
        messages.success(request, ("Cannot remove invoice from completed Model"))
        return redirect(request.META.get("HTTP_REFERER"))
    get_status = Status.objects.get(name="Invoiced")
    invoice.status = get_status
    invoice.save()
    dispatch_number = invoice.dispatch_number
    status = invoice.status
    customer = invoice.customer
    date_received = invoice.date_received
    date_invoiced = invoice.date_invoiced
    note = invoice.note
    amount = invoice.amount
    process_invoice = RelyProcessed.objects.create(
            dispatch_number = dispatch_number,
            status=status,
            customer=customer,
            date_received=date_received,
            date_invoiced=date_invoiced,
            note=note,
            amount=amount
    )
    process_invoice.save()
    del_invoice = get_object_or_404(RelyInvoice, id=invoice.id)
    del_invoice.delete()
    messages.success(request, ("Invoice Status updated."))
    return redirect(request.META.get("HTTP_REFERER"))

def added_status(request, pk):
    try:
        invoice = get_object_or_404(RelyCompleted, id=pk)
    except:
        messages.success(request, ("Cannot move invoice from paid Model."))
        return redirect(request.META.get("HTTP_REFERER"))
    get_status = Status.objects.get(name="Added")
    invoice.status = get_status
    invoice.save()
    dispatch_number = invoice.dispatch_number
    status = invoice.status
    customer = invoice.customer
    date_received = invoice.date_received
    date_invoiced = invoice.date_invoiced
    note = invoice.note
    amount = invoice.amount
    new_invoice = RelyInvoice.objects.create(
            dispatch_number = dispatch_number,
            status=status,
            customer=customer,
            date_received=date_received,
            date_invoiced=date_invoiced,
            note=note,
            amount=amount
    )
    del_invoice = get_object_or_404(RelyCompleted, id=invoice.id)
    del_invoice.delete()
    messages.success(request, ("Invoice Status updated."))
    return redirect(request.META.get("HTTP_REFERER"))

def added_paid_status(request, pk):
    try:
        invoice = get_object_or_404(RelyPaid, id=pk)
    except:
        messages.success(request, ("Cannot move invoice from paid Model."))
        return redirect(request.META.get("HTTP_REFERER"))
    get_status = Status.objects.get(name="Added")
    invoice.status = get_status
    invoice.save()
    dispatch_number = invoice.dispatch_number
    status = invoice.status
    customer = invoice.customer
    date_received = invoice.date_received
    date_invoiced = invoice.date_invoiced
    note = invoice.note
    amount = invoice.amount
    new_invoice = RelyInvoice.objects.create(
            dispatch_number = dispatch_number,
            status=status,
            customer=customer,
            date_received=date_received,
            date_invoiced=date_invoiced,
            note=note,
            amount=amount
    )
    del_invoice = get_object_or_404(RelyPaid, id=invoice.id)
    del_invoice.delete()
    messages.success(request, ("Invoice Status updated."))
    return redirect(request.META.get("HTTP_REFERER"))

def added_problem_status(request, pk):
    try:
        invoice = get_object_or_404(RelyProblem, id=pk)
    except:
        messages.success(request, ("Cannot move invoice from paid Model."))
        return redirect(request.META.get("HTTP_REFERER"))
    get_status = Status.objects.get(name="Added")
    invoice.status = get_status
    invoice.save()
    dispatch_number = invoice.dispatch_number
    status = invoice.status
    customer = invoice.customer
    date_received = invoice.date_received
    date_invoiced = invoice.date_invoiced
    note = invoice.note
    amount = invoice.amount
    new_invoice = RelyInvoice.objects.create(
            dispatch_number = dispatch_number,
            status=status,
            customer=customer,
            date_received=date_received,
            date_invoiced=date_invoiced,
            note=note,
            amount=amount
    )
    del_invoice = get_object_or_404(RelyProblem, id=invoice.id)
    del_invoice.delete()
    messages.success(request, ("Invoice Status updated."))
    return redirect(request.META.get("HTTP_REFERER"))

def completed_status(request, pk):
    invoice = get_object_or_404(RelyInvoice, id=pk)
    get_status = Status.objects.get(name="Completed")
    invoice.status = get_status
    invoice.save()
    dispatch_number = invoice.dispatch_number
    status = invoice.status
    customer = invoice.customer
    date_received = invoice.date_received
    date_invoiced = invoice.date_invoiced
    note = invoice.note
    amount = invoice.amount
    process_invoice = RelyCompleted.objects.create(
            dispatch_number = dispatch_number,
            status=status,
            customer=customer,
            date_received=date_received,
            note=note,
            amount=0
    )
    process_invoice.save()
    del_invoice = get_object_or_404(RelyInvoice, id=invoice.id)
    del_invoice.delete()
    messages.success(request, ("Invoice Status updated."))
    return redirect(request.META.get("HTTP_REFERER"))

def rely_invoice_processed(request):
    all_invoice = RelyProcessed.objects.all().order_by('-id')
    all_statuses = Status.objects.all()
    search_results = None
    if request.method == "POST":
        inv_data = request.POST.get('inv_data', '').strip()
        messages.success(request, f"You searched {inv_data}")
        if inv_data:
            search_results = RelyProcessed.objects.filter(dispatch_number__icontains=inv_data) | \
                             RelyProcessed.objects.filter(customer__icontains=inv_data)
    context = {
        "all_invoice": all_invoice,
        "all_statuses": all_statuses,
        'search_results':search_results
    }
    return render(request, 'rely_inv_pro.html', context) 

def denied_status(request, pk):
    invoice = get_object_or_404(RelyInvoice, id=pk)
    get_status = Status.objects.get(name="Denied")
    invoice.status = get_status
    invoice.save()
    dispatch_number = invoice.dispatch_number
    status = invoice.status
    customer = invoice.customer
    date_received = invoice.date_received
    date_invoiced = invoice.date_invoiced
    note = invoice.note
    amount = invoice.amount
    process_invoice = RelyCompleted.objects.create(
            dispatch_number = dispatch_number,
            status=status,
            customer=customer,
            date_received=date_received,
            note=note,
            amount=0
    )
    process_invoice.save()
    del_invoice = get_object_or_404(RelyInvoice, id=invoice.id)
    del_invoice.delete()
    messages.success(request, ("Invoice Status updated."))
    return redirect(request.META.get("HTTP_REFERER"))

def cancelled_status(request, pk):
    invoice = get_object_or_404(RelyInvoice, id=pk)
    get_status = Status.objects.get(name="Cancelled")
    invoice.status = get_status
    invoice.save()
    dispatch_number = invoice.dispatch_number
    status = invoice.status
    customer = invoice.customer
    date_received = invoice.date_received
    date_invoiced = invoice.date_invoiced
    note = invoice.note
    amount = invoice.amount
    process_invoice = RelyCompleted.objects.create(
            dispatch_number = dispatch_number,
            status=status,
            customer=customer,
            date_received=date_received,
            note=note,
            amount=0
    )
    process_invoice.save()
    del_invoice = get_object_or_404(RelyInvoice, id=invoice.id)
    del_invoice.delete()
    messages.success(request, ("Invoice Status updated."))
    return redirect(request.META.get("HTTP_REFERER"))

def paid_status(request, pk):
    invoice = get_object_or_404(RelyProcessed, id=pk)
    get_status = Status.objects.get(name="Paid")
    invoice.status = get_status
    invoice.save()
    dispatch_number = invoice.dispatch_number
    status = invoice.status
    customer = invoice.customer
    date_received = invoice.date_received
    date_invoiced = invoice.date_invoiced
    note = invoice.note
    amount = invoice.amount
    process_invoice = RelyPaid.objects.create(
            dispatch_number = dispatch_number,
            status=status,
            customer=customer,
            date_received=date_received,
            note=note,
            amount=0
    )
    process_invoice.save()
    del_invoice = get_object_or_404(RelyProcessed, id=invoice.id)
    del_invoice.delete()
    messages.success(request, ("Invoice Status updated."))
    return redirect(request.META.get("HTTP_REFERER"))

def paid_problem_status(request, pk):
    invoice = get_object_or_404(RelyProblem, id=pk)
    get_status = Status.objects.get(name="Paid")
    invoice.status = get_status
    invoice.save()
    dispatch_number = invoice.dispatch_number
    status = invoice.status
    customer = invoice.customer
    date_received = invoice.date_received
    date_invoiced = invoice.date_invoiced
    note = invoice.note
    amount = invoice.amount
    process_invoice = RelyPaid.objects.create(
            dispatch_number = dispatch_number,
            status=status,
            customer=customer,
            date_received=date_received,
            note=note,
            amount=0
    )
    process_invoice.save()
    del_invoice = get_object_or_404(RelyProblem, id=invoice.id)
    del_invoice.delete()
    messages.success(request, ("Invoice Status updated."))
    return redirect(request.META.get("HTTP_REFERER"))

def problem_status(request, pk):
    invoice = get_object_or_404(RelyPaid, id=pk)
    get_status = Status.objects.get(name="Problem")
    invoice.status = get_status
    invoice.save()
    dispatch_number = invoice.dispatch_number
    status = invoice.status
    customer = invoice.customer
    date_received = invoice.date_received
    date_invoiced = invoice.date_invoiced
    note = invoice.note
    amount = invoice.amount
    new_invoice = RelyProblem.objects.create(
            dispatch_number = dispatch_number,
            status=status,
            customer=customer,
            date_received=date_received,
            date_invoiced=date_invoiced,
            note=note,
            amount=amount
    )
    del_invoice = get_object_or_404(RelyPaid, id=invoice.id)
    del_invoice.delete()
    messages.success(request, ("Invoice Status updated."))
    return redirect(request.META.get("HTTP_REFERER"))

def problem_inv_status(request, pk):
    invoice = get_object_or_404(RelyProcessed, id=pk)
    get_status = Status.objects.get(name="Problem")
    invoice.status = get_status
    invoice.save()
    dispatch_number = invoice.dispatch_number
    status = invoice.status
    customer = invoice.customer
    date_received = invoice.date_received
    date_invoiced = invoice.date_invoiced
    note = invoice.note
    amount = invoice.amount
    new_invoice = RelyProblem.objects.create(
            dispatch_number = dispatch_number,
            status=status,
            customer=customer,
            date_received=date_received,
            date_invoiced=date_invoiced,
            note=note,
            amount=amount
    )
    del_invoice = get_object_or_404(RelyProcessed, id=invoice.id)
    del_invoice.delete()
    messages.success(request, ("Invoice Status updated."))
    return redirect(request.META.get("HTTP_REFERER"))

def rely_invoice_completed(request):
    all_invoice = RelyCompleted.objects.all().order_by('-id')
    all_statuses = Status.objects.all()
    search_results = None
    if request.method == "POST":
        inv_data = request.POST.get('inv_data', '').strip()
        messages.success(request, f"You searched {inv_data}")
        
        if inv_data:
            search_results = RelyCompleted.objects.filter(dispatch_number__icontains=inv_data) | \
                             RelyCompleted.objects.filter(customer__icontains=inv_data)
    context = {
        "all_invoice": all_invoice,
        "all_statuses": all_statuses,
        'search_results':search_results
    }
    return render(request, 'rely_completed.html', context) 

def rely_invoice_paid(request):
    all_invoice = RelyPaid.objects.all().order_by('-id')
    all_statuses = Status.objects.all()
    search_results = None
    if request.method == "POST":
        inv_data = request.POST.get('inv_data', '').strip()
        messages.success(request, f"You searched {inv_data}")
        
        if inv_data:
            search_results = RelyPaid.objects.filter(dispatch_number__icontains=inv_data) | \
                             RelyPaid.objects.filter(customer__icontains=inv_data)
    context = {
        "all_invoice": all_invoice,
        "all_statuses": all_statuses,
        'search_results':search_results
    }
    return render(request, 'rely_paid.html', context) 

def rely_invoice_problem(request):
    all_invoice = RelyProblem.objects.all().order_by('-id')
    all_statuses = Status.objects.all()
    search_results = None
    if request.method == "POST":
        inv_data = request.POST.get('inv_data', '').strip()
        messages.success(request, f"You searched {inv_data}")
        
        if inv_data:
            search_results = RelyProblem.objects.filter(dispatch_number__icontains=inv_data) | \
                             RelyProblem.objects.filter(customer__icontains=inv_data)
    context = {
        "all_invoice": all_invoice,
        "all_statuses": all_statuses,
        'search_results':search_results
    }
    return render(request, 'rely_problem.html', context) 
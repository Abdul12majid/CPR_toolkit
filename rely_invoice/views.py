from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .models import RelyInvoice, Status
from django.contrib import messages 
from django.contrib.auth.decorators import login_required
from django.utils.timezone import make_aware, datetime

# Create your views here.
def rely_invoice(request):
    all_invoice = RelyInvoice.objects.all().order_by('-id')
    all_statuses = Status.objects.all()
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
        return redirect('rely_invoice')
    return render(request, 'update_r_invoice.html', context)

@login_required(login_url='login')
def delete_r_invoice(request, pk):
    invoice = get_object_or_404(RelyInvoice, id=pk)
    invoice.delete()
    return redirect(request.META.get("HTTP_REFERER"))
    return redirect("rely_invoice")


def update_status(request, pk):
    invoice = get_object_or_404(RelyInvoice, id=pk)
    get_status = Status.objects.get(id=1)
    invoice.status = get_status
    invoice.save()
    messages.success(request, ("Invoice Status updated."))
    return redirect(request.META.get("HTTP_REFERER"))

def added_status(request, pk):
    invoice = get_object_or_404(RelyInvoice, id=pk)
    get_status = Status.objects.get(id=4)
    invoice.status = get_status
    invoice.save()
    messages.success(request, ("Invoice Status updated."))
    return redirect(request.META.get("HTTP_REFERER"))

def paid_status(request, pk):
    invoice = get_object_or_404(RelyInvoice, id=pk)
    get_status = Status.objects.get(id=3)
    invoice.status = get_status
    invoice.save()
    messages.success(request, ("Invoice Status updated."))
    return redirect(request.META.get("HTTP_REFERER"))
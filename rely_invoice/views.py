from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .models import RelyInvoice, Status, RelyProcessed, RelyCompleted
from .models import RelyPaid, RelyProblem, RelyReassigned, RelyGMMM
from django.contrib import messages 
from django.contrib.auth.decorators import login_required
from django.utils.timezone import make_aware, datetime
from django.utils.timezone import now
import pytz
from django.db.models import Sum, Avg, F
from django.core.paginator import Paginator
from django.utils import timezone
from django.utils.timezone import localtime
from datetime import timedelta


# Create your views here.
def rely_invoice(request):
    all_invoice = RelyInvoice.objects.all().order_by('-id')
    all_statuses = Status.objects.all()
    pst_tz = pytz.timezone("America/Los_Angeles")
    now_pst = now().astimezone(pst_tz)
    print(now_pst, flush=True)
    search_results = None
    the_result = None
    if request.method == "POST":
        check_data = request.POST.get('inv_data', '').strip()
        if check_data != "":
            print("Invoice", flush=True)
            inv_data = request.POST.get('inv_data', '').strip()
            messages.success(request, f"You searched {inv_data}")
            
            if inv_data:
                search_results = RelyInvoice.objects.filter(dispatch_number__icontains=inv_data) | \
                                 RelyInvoice.objects.filter(customer__icontains=inv_data)
        else:
            print("Not Invoice", flush=True)
            inv_data = request.POST.get('other_data', '').strip()
            messages.success(request, f"You searched {inv_data}")
            
            if inv_data:
                the_result1 = RelyProcessed.objects.filter(dispatch_number__icontains=inv_data) | \
                              RelyProcessed.objects.filter(customer__icontains=inv_data)
                the_result2 = RelyPaid.objects.filter(dispatch_number__icontains=inv_data) | \
                              RelyPaid.objects.filter(customer__icontains=inv_data)
                the_result3 = RelyCompleted.objects.filter(dispatch_number__icontains=inv_data) | \
                              RelyCompleted.objects.filter(customer__icontains=inv_data)
                the_result4 = RelyReassigned.objects.filter(dispatch_number__icontains=inv_data) | \
                              RelyReassigned.objects.filter(customer__icontains=inv_data)
                the_result5 = RelyProblem.objects.filter(dispatch_number__icontains=inv_data) | \
                              RelyProblem.objects.filter(customer__icontains=inv_data)
                the_result  = list(the_result1) + list(the_result2) + list(the_result3) + list(the_result4) + list(the_result5)

    context = {
        "all_invoice": all_invoice,
        "all_statuses": all_statuses,
        'search_results':search_results,
        "the_result":the_result,
        
    }
    return render(request, 'rely_inv.html', context) 

@login_required(login_url='login')
def update_r_invoice(request, pk):
    get_invoice = RelyInvoice.objects.get(id=pk)
    inv_id = get_invoice.id
    get_status = Status.objects.get(name="Invoiced")
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
        get_invoice.dispatch_number = dispatch_no
        get_invoice.customer = customer
        get_invoice.note = note
        get_invoice.amount = float(inv_amount)
        get_invoice.date_invoiced = date_added
        get_invoice.date_received = date_received
        get_invoice.save()
        messages.success(request, ("Invoice updated."))
        #sending to invoice model
        invoiced = RelyProcessed.objects.create(
            dispatch_number = get_invoice.dispatch_number,
            status=get_status,
            customer=get_invoice.customer,
            date_invoiced=get_invoice.date_invoiced,
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
    invoice = get_object_or_404(RelyProcessed, id=pk)
    get_status = Status.objects.get(name="Invoiced")
    invoice.status = get_status
    invoice.save()
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

def update_processed_paid(request, pk):
    get_invoice = RelyProcessed.objects.get(id=pk)
    inv_id = get_invoice.id
    get_status = Status.objects.get(name="Paid")
    print(f"Before Update:- {get_invoice.date_paid}", flush=True)
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
        date_paid_str = request.POST.get('date_paid')
        date_added = datetime.strptime(date_added_str, "%Y-%m-%d").date() if date_added_str else today.date()
        date_received = datetime.strptime(date_received_str, "%Y-%m-%d").date() if date_received_str else today.date()
        date_paid = datetime.strptime(date_paid_str, "%Y-%m-%d").date() if date_paid_str else today.date()
        get_invoice.dispatch_number = dispatch_no
        get_invoice.customer = customer
        get_invoice.note = note
        get_invoice.amount = float(inv_amount)
        get_invoice.date_invoiced = date_added
        get_invoice.date_received = date_received
        get_invoice.date_paid = date_paid
        get_invoice.save()
        print(f"After Update:- {get_invoice.date_paid}", flush=True)
        messages.success(request, ("Invoice updated."))
        #sending to invoice model
        invoiced = RelyPaid.objects.create(
            dispatch_number = get_invoice.dispatch_number,
            status=get_status,
            customer=get_invoice.customer,
            date_invoiced=get_invoice.date_invoiced,
            date_received=get_invoice.date_received,
            note=get_invoice.note,
            amount=get_invoice.amount,
            date_paid=get_invoice.date_paid
        )
        invoiced.save()
        get_invoice.delete()
        return redirect('rely_invoice_processed')
    return render(request, 'update_paid_invoice.html', context)

def added_reassign_status(request, pk):
    invoice = get_object_or_404(RelyInvoice, id=pk)
    get_status = Status.objects.get(name="Reassigned")
    invoice.status = get_status
    invoice.save()
    dispatch_number = invoice.dispatch_number
    status = invoice.status
    customer = invoice.customer
    date_received = invoice.date_received
    date_invoiced = invoice.date_invoiced
    note = invoice.note
    amount = invoice.amount
    new_invoice = RelyReassigned.objects.create(
            dispatch_number = dispatch_number,
            status=status,
            customer=customer,
            date_received=date_received,
            date_invoiced=date_invoiced,
            note=note,
            amount=amount
    )
    del_invoice = get_object_or_404(RelyInvoice, id=invoice.id)
    del_invoice.delete()
    messages.success(request, ("Invoice Status updated."))
    return redirect(request.META.get("HTTP_REFERER"))

def added_problem_status(request, pk):
    invoice = get_object_or_404(RelyInvoice, id=pk)
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
    del_invoice = get_object_or_404(RelyInvoice, id=invoice.id)
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
            amount=amount
    )
    process_invoice.save()
    del_invoice = get_object_or_404(RelyInvoice, id=invoice.id)
    del_invoice.delete()
    messages.success(request, ("Invoice Status updated."))
    return redirect(request.META.get("HTTP_REFERER"))

def completed_reassigned_status(request, pk):
    invoice = get_object_or_404(RelyCompleted, id=pk)
    get_status = Status.objects.get(name="Reassigned")
    invoice.status = get_status
    invoice.save()
    dispatch_number = invoice.dispatch_number
    status = invoice.status
    customer = invoice.customer
    date_received = invoice.date_received
    date_invoiced = invoice.date_invoiced
    note = invoice.note
    amount = invoice.amount
    process_invoice = RelyReassigned.objects.create(
            dispatch_number = dispatch_number,
            status=status,
            customer=customer,
            date_received=date_received,
            note=note,
            amount=amount
    )
    process_invoice.save()
    del_invoice = get_object_or_404(RelyCompleted, id=invoice.id)
    del_invoice.delete()
    messages.success(request, ("Invoice Status updated."))
    return redirect(request.META.get("HTTP_REFERER"))

def completed_problem_status(request, pk):
    invoice = get_object_or_404(RelyCompleted, id=pk)
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
    process_invoice = RelyProblem.objects.create(
            dispatch_number = dispatch_number,
            status=status,
            customer=customer,
            date_received=date_received,
            note=note,
            amount=amount
    )
    process_invoice.save()
    del_invoice = get_object_or_404(RelyCompleted, id=invoice.id)
    del_invoice.delete()
    messages.success(request, ("Invoice Status updated."))
    return redirect(request.META.get("HTTP_REFERER"))

def completed_denied_status(request, pk):
    invoice = get_object_or_404(RelyCompleted, id=pk)
    get_status = Status.objects.get(name="Denied")
    invoice.status = get_status
    invoice.save()
    messages.success(request, ("Invoice Status updated."))
    return redirect(request.META.get("HTTP_REFERER"))

def completed_cancelled_status(request, pk):
    invoice = get_object_or_404(RelyCompleted, id=pk)
    get_status = Status.objects.get(name="Cancelled")
    invoice.status = get_status
    invoice.save()
    messages.success(request, ("Invoice Status updated."))
    return redirect(request.META.get("HTTP_REFERER"))

def processed_reassigned_status(request, pk):
    invoice = get_object_or_404(RelyProcessed, id=pk)
    get_status = Status.objects.get(name="Reassigned")
    invoice.status = get_status
    invoice.save()
    dispatch_number = invoice.dispatch_number
    status = invoice.status
    customer = invoice.customer
    date_received = invoice.date_received
    date_invoiced = invoice.date_invoiced
    note = invoice.note
    amount = invoice.amount
    process_invoice = RelyReassigned.objects.create(
            dispatch_number = dispatch_number,
            status=status,
            customer=customer,
            date_received=date_received,
            date_invoiced=date_invoiced,
            note=note,
            amount=amount
    )
    process_invoice.save()
    del_invoice = get_object_or_404(RelyProcessed, id=invoice.id)
    del_invoice.delete()
    messages.success(request, ("Invoice Status updated."))
    return redirect(request.META.get("HTTP_REFERER"))

def reassigned_added_status(request, pk):
    invoice = get_object_or_404(RelyReassigned, id=pk)
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
    process_invoice = RelyInvoice.objects.create(
            dispatch_number = dispatch_number,
            status=status,
            customer=customer,
            date_received=date_received,
            date_invoiced=date_invoiced,
            note=note,
            amount=amount
    )
    process_invoice.save()
    del_invoice = get_object_or_404(RelyReassigned, id=invoice.id)
    del_invoice.delete()
    messages.success(request, ("Invoice Status updated."))
    return redirect(request.META.get("HTTP_REFERER"))

def rely_invoice_processed(request):
    all_invoice = RelyProcessed.objects.all().order_by('date_invoiced')
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
    search_results = None

    # Helper function to calculate average and total amounts
    def get_avg_total(queryset):
        total = queryset.aggregate(total=Sum('amount'))['total'] or 0
        avg = queryset.aggregate(avg=Avg('amount'))['avg'] or 0
        return round(avg, 2), round(total, 2)

    # Calculate average and total amounts for different time ranges
    current_day_avg, current_day_total = get_avg_total(
        RelyProcessed.objects.filter(date_invoiced__gte=current_day).exclude(amount=0)
    )
    seven_day_avg, seven_day_total = get_avg_total(
        RelyProcessed.objects.filter(date_invoiced__gte=seven_days_ago).exclude(amount=0)
    )
    thirty_day_avg, thirty_day_total = get_avg_total(
        RelyProcessed.objects.filter(date_invoiced__gte=thirty_days_ago).exclude(amount=0)
    )
    six_month_avg, six_month_total = get_avg_total(
        RelyProcessed.objects.filter(date_invoiced__gte=six_months_ago).exclude(amount=0)
    )
    twelve_month_avg, twelve_month_total = get_avg_total(
        RelyProcessed.objects.filter(date_invoiced__gte=twelve_months_ago).exclude(amount=0)
    )
    paginate = Paginator(all_invoice, 20)
    page = request.GET.get('page')
    invoices = paginate.get_page(page)

    # Helper function to calculate average days difference
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

    # Helper function to calculate average due_days
    def get_avg_due_days(queryset):
        total_due_days = 0
        count = 0
        for invoice in queryset:
            if invoice.due_days is not None:
                total_due_days += invoice.due_days
                count += 1
        return round(total_due_days / count, 2) if count > 0 else 0

    # Calculate average days difference for different time ranges
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

    # Calculate average due_days for different time ranges
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

    # Calculate overall averages
    overall_avg_days = get_avg_days(RelyProcessed.objects.exclude(amount=0))
    overall_avg_due_days = get_avg_due_days(RelyProcessed.objects.exclude(amount=0))
    overall_total = RelyProcessed.objects.aggregate(total=Sum('amount'))['total'] or 0
    overall_total = round(overall_total, 2)

    # Handle search functionality
    if request.method == "POST":
        inv_data = request.POST.get('inv_data', '').strip()
        messages.success(request, f"You searched {inv_data}")
        if inv_data:
            search_results = RelyProcessed.objects.filter(dispatch_number__icontains=inv_data) | \
                            RelyProcessed.objects.filter(customer__icontains=inv_data)

    # Prepare context for rendering the template
    context = {
        "all_invoice": all_invoice,
        "all_statuses": all_statuses,
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
        "current_day_avg_days": current_day_avg_days,
        "seven_day_avg_days": seven_day_avg_days,
        "thirty_day_avg_days": thirty_day_avg_days,
        "six_month_avg_days": six_month_avg_days,
        "twelve_month_avg_days": twelve_month_avg_days,
        "overall_avg_days": overall_avg_days,
        "overall_total": overall_total,
        "current_day_avg_due_days": current_day_avg_due_days,
        "seven_day_avg_due_days": seven_day_avg_due_days,
        "thirty_day_avg_due_days": thirty_day_avg_due_days,
        "six_month_avg_due_days": six_month_avg_due_days,
        "twelve_month_avg_due_days": twelve_month_avg_due_days,
        "overall_avg_due_days": overall_avg_due_days,
        "invoices":invoices,
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
            amount=amount
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
            amount=amount
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
            amount=amount
    )
    process_invoice.save()
    del_invoice = get_object_or_404(RelyProcessed, id=invoice.id)
    del_invoice.delete()
    messages.success(request, ("Invoice Status updated."))
    return redirect(request.META.get("HTTP_REFERER"))

def paid_reassigned_status(request, pk):
    invoice = get_object_or_404(RelyPaid, id=pk)
    get_status = Status.objects.get(name="Reassigned")
    invoice.status = get_status
    invoice.save()
    dispatch_number = invoice.dispatch_number
    status = invoice.status
    customer = invoice.customer
    date_received = invoice.date_received
    date_invoiced = invoice.date_invoiced
    note = invoice.note
    amount = invoice.amount
    process_invoice = RelyReassigned.objects.create(
            dispatch_number = dispatch_number,
            status=status,
            customer=customer,
            date_received=date_received,
            date_invoiced=date_invoiced,
            note=note,
            amount=amount
    )
    process_invoice.save()
    del_invoice = get_object_or_404(RelyPaid, id=invoice.id)
    del_invoice.delete()
    messages.success(request, ("Invoice Status updated."))
    return redirect(request.META.get("HTTP_REFERER"))

def reassigned_paid_status(request, pk):
    invoice = get_object_or_404(RelyReassigned, id=pk)
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
            amount=amount
    )
    process_invoice.save()
    del_invoice = get_object_or_404(RelyReassigned, id=invoice.id)
    del_invoice.delete()
    messages.success(request, ("Invoice Status updated."))
    return redirect(request.META.get("HTTP_REFERER"))

def problem_paid_status(request, pk):
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
            amount=amount
    )
    process_invoice.save()
    del_invoice = get_object_or_404(RelyProblem, id=invoice.id)
    del_invoice.delete()
    messages.success(request, ("Invoice Status updated."))
    return redirect(request.META.get("HTTP_REFERER"))

def problem_added_status(request, pk):
    invoice = get_object_or_404(RelyProblem, id=pk)
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
    process_invoice = RelyInvoice.objects.create(
            dispatch_number = dispatch_number,
            status=status,
            customer=customer,
            date_received=date_received,
            date_invoiced=date_invoiced,
            note=note,
            amount=amount
    )
    process_invoice.save()
    del_invoice = get_object_or_404(RelyProblem, id=invoice.id)
    del_invoice.delete()
    messages.success(request, ("Invoice Status updated."))
    return redirect(request.META.get("HTTP_REFERER"))

def problem_invoice_status(request, pk):
    invoice = get_object_or_404(RelyProblem, id=pk)
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
    del_invoice = get_object_or_404(RelyProblem, id=invoice.id)
    del_invoice.delete()
    messages.success(request, ("Invoice Status updated."))
    return redirect(request.META.get("HTTP_REFERER"))

def problem_completed_status(request, pk):
    invoice = get_object_or_404(RelyProblem, id=pk)
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
            amount=amount
    )
    process_invoice.save()
    del_invoice = get_object_or_404(RelyProblem, id=invoice.id)
    del_invoice.delete()
    messages.success(request, ("Invoice Status updated."))
    return redirect(request.META.get("HTTP_REFERER"))

def problem_denied_status(request, pk):
    invoice = get_object_or_404(RelyProblem, id=pk)
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
            amount=amount
    )
    process_invoice.save()
    del_invoice = get_object_or_404(RelyProblem, id=invoice.id)
    del_invoice.delete()
    messages.success(request, ("Invoice Status updated."))
    return redirect(request.META.get("HTTP_REFERER"))

def problem_cancelled_status(request, pk):
    invoice = get_object_or_404(RelyProblem, id=pk)
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
            amount=amount
    )
    process_invoice.save()
    del_invoice = get_object_or_404(RelyProblem, id=invoice.id)
    del_invoice.delete()
    messages.success(request, ("Invoice Status updated."))
    return redirect(request.META.get("HTTP_REFERER"))

def problem_reassigned_status(request, pk):
    invoice = get_object_or_404(RelyProblem, id=pk)
    get_status = Status.objects.get(name="Reassigned")
    invoice.status = get_status
    invoice.save()
    dispatch_number = invoice.dispatch_number
    status = invoice.status
    customer = invoice.customer
    date_received = invoice.date_received
    date_invoiced = invoice.date_invoiced
    note = invoice.note
    amount = invoice.amount
    process_invoice = RelyReassigned.objects.create(
            dispatch_number = dispatch_number,
            status=status,
            customer=customer,
            date_received=date_received,
            date_invoiced=date_invoiced,
            note=note,
            amount=amount
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

def rely_invoice_reassign(request):
    all_invoice = RelyReassigned.objects.all().order_by('-id')
    all_gmmm_invoice = RelyGMMM.objects.all().order_by('-id')
    total = list(all_invoice) + list(all_gmmm_invoice)
    all_statuses = Status.objects.all()
    total_amount = RelyReassigned.get_total_amount()
    total_gmmm_amount = RelyGMMM.get_total_amount()
    diff = total_amount - total_gmmm_amount
    check_str = str(diff)
    negative = "-" in check_str
    search_results = None

    if request.method == "POST":
        inv_data = request.POST.get('inv_data', '').strip()
        messages.success(request, f"You searched {inv_data}")
        if inv_data:
            # Search in RelyReassigned model
            rely_reassigned_results = RelyReassigned.objects.filter(
                dispatch_number__icontains=inv_data
            ) | RelyReassigned.objects.filter(
                customer__icontains=inv_data
            )

            # Search in RelyGMMM model
            rely_gmmm_results = RelyGMMM.objects.filter(
                dispatch_number__icontains=inv_data
            ) | RelyGMMM.objects.filter(
                customer__icontains=inv_data
            )

            # Combine the results into a list
            search_results = list(rely_reassigned_results) + list(rely_gmmm_results)

    context = {
        "all_invoice": all_invoice,
        "total": total,
        "all_statuses": all_statuses,
        'search_results': search_results,
        "total_amount": total_amount,
        "total_gmmm_amount": total_gmmm_amount,
        "diff": diff,
        "negative": negative
    }
    return render(request, 'rely_reassign.html', context)

def move_dispatches(request):
    if request.method == 'POST':
        dispatch_numbers = request.POST.get('dispatch_numbers', '').split(',')
        dispatch_numbers = [num.strip() for num in dispatch_numbers if num.strip()]
        get_status = Status.objects.get(name="Paid")
        
        if dispatch_numbers:
            # Retrieve records from RelyProcessed
            records_to_move = RelyProcessed.objects.filter(dispatch_number__in=dispatch_numbers)
            
            if not records_to_move.exists():
                print("No records found with the provided dispatch numbers.", flush=True)
            
            # Copy records to RelyNew
            for record in records_to_move:
                try:
                    RelyPaid.objects.create(
                        dispatch_number=record.dispatch_number,
                        status=get_status,
                        customer=record.customer,
                        date_received=record.date_received,
                        date_invoiced=record.date_invoiced,
                        note=record.note,
                        amount=record.amount
                    )

                    print(f"Record with dispatch_number {record.dispatch_number} copied to RelyPaid.")
                except Exception as e:
                    print(f"Error copying record with dispatch_number {record.dispatch_number}: {e}")
                    
            
            # Delete records from RelyProcessed
            deleted_count, _ = records_to_move.delete()
            messages.success(request, ("Invoice Status updated"))
            print(f"Successfully moved {deleted_count} records to RelyNew and deleted them from RelyProcessed.", flush=True)
            return redirect(request.META.get("HTTP_REFERER"))
        else:
            print("No valid dispatch numbers provided.", flush=True)
            return redirect(request.META.get("HTTP_REFERER"))
    
    return render(request, 'test_move.html')

def make_invoice(request):
    status = Status.objects.get(name="Added")
    pst_tz = pytz.timezone("America/Los_Angeles")
    now_pst = now().astimezone(pst_tz)
    today_default = timezone.now().astimezone(pst_tz)
    today = now_pst.date()
    context = {
        "today_date": today_default.strftime("%Y-%m-%d")
    }
    if request.method=="POST":
        dispatch_number = request.POST.get('dispatch_no')
        customer = request.POST.get('name')
        inv_amount = request.POST.get('invoiced_amount')
        note = request.POST.get('note')
        date_added_str = request.POST.get('date_added')
        date_received_str = request.POST.get('date_received')
        date_added = datetime.strptime(date_added_str, "%Y-%m-%d").date() if date_added_str else today
        date_received = datetime.strptime(date_received_str, "%Y-%m-%d").date() if date_received_str else today
        invoiced = RelyInvoice.objects.create(
            dispatch_number = dispatch_number,
            status=status,
            customer=customer,
            date_received=date_received,
            note=note,
            amount=inv_amount
        )
        invoiced.save()
        messages.success(request, (f"{customer} Invoice Added."))
        return redirect('rely_invoice')
    return render(request, "make_invoice.html", context)

def make_reassigned_invoice(request):
    status = Status.objects.get(name="Reassigned")
    pst_tz = pytz.timezone("America/Los_Angeles")
    now_pst = now().astimezone(pst_tz)
    today_default = timezone.now().astimezone(pst_tz)
    today = now_pst.date()
    context = {
        "today_date": today_default.strftime("%Y-%m-%d")
    }
    if request.method=="POST":
        dispatch_number = request.POST.get('dispatch_no')
        customer = request.POST.get('name')
        inv_amount = request.POST.get('invoiced_amount')
        note = request.POST.get('note')
        date_added_str = request.POST.get('date_added')
        date_received_str = request.POST.get('date_received')
        date_added = datetime.strptime(date_added_str, "%Y-%m-%d").date() if date_added_str else today
        date_received = datetime.strptime(date_received_str, "%Y-%m-%d").date() if date_received_str else today
        invoiced = RelyReassigned.objects.create(
            dispatch_number = dispatch_number,
            status=status,
            customer=customer,
            date_received=date_received,
            note=note,
            amount=inv_amount
        )
        invoiced.save()
        messages.success(request, (f"{customer} Invoice Added."))
        return redirect('rely_invoice_reassign')
    return render(request, "make_reassigned_invoice.html", context)

def make_gmmm_invoice(request):
    status = Status.objects.get(name="GMMM")
    pst_tz = pytz.timezone("America/Los_Angeles")
    now_pst = now().astimezone(pst_tz)
    today_default = timezone.now().astimezone(pst_tz)
    today = now_pst.date()
    context = {
        "today_date": today_default.strftime("%Y-%m-%d")
    }
    if request.method=="POST":
        dispatch_number = request.POST.get('dispatch_no')
        customer = request.POST.get('name')
        inv_amount = request.POST.get('invoiced_amount')
        note = request.POST.get('note')
        date_added_str = request.POST.get('date_added')
        date_received_str = request.POST.get('date_received')
        date_added = datetime.strptime(date_added_str, "%Y-%m-%d").date() if date_added_str else today
        date_received = datetime.strptime(date_received_str, "%Y-%m-%d").date() if date_received_str else today
        invoiced = RelyGMMM.objects.create(
            dispatch_number = dispatch_number,
            status=status,
            customer=customer,
            date_received=date_received,
            note=note,
            amount=inv_amount
        )
        invoiced.save()
        messages.success(request, (f"{customer} Invoice Added."))
        return redirect('rely_invoice_reassign')
    return render(request, "make_rely_gmmm.html", context)

#0135788,12345,5678912
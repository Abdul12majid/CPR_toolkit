from django.shortcuts import render, HttpResponse
from .models import RelyInvoice, Status

# Create your views here.
def rely_invoice(request):
    all_invoice = RelyInvoice.objects.all()
    all_statuses = Status.objects.all()
    context = {
        "all_invoice": all_invoice,
        "all_statuses": all_statuses,
    }
    return render(request, 'rely_inv.html', context)

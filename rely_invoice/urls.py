from . import views
from django.urls import path

urlpatterns = [
    path('rely_invoice', views.rely_invoice, name="rely_invoice"),
    path('update_r_invoice/<int:pk>', views.update_r_invoice, name="update_r_invoice"),
    path('delete_r_invoice/<int:pk>', views.delete_r_invoice, name="delete_r_invoice"),
    path('invoice_status/<int:pk>', views.invoice_status, name="invoice_status"),
    path('added_status/<int:pk>', views.added_status, name="added_status"),
    path('completed_status/<int:pk>', views.completed_status, name="completed_status"),
    path('rely_invoice_processed', views.rely_invoice_processed, name="rely_invoice_processed"),
    path('rely_invoice_completed', views.rely_invoice_completed, name="rely_invoice_completed"),
]
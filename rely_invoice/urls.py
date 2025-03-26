from . import views
from django.urls import path

urlpatterns = [
    path('rely_invoice', views.rely_invoice, name="rely_invoice"),
    path('make_invoice', views.make_invoice, name="make_invoice"),
    path('make_gmmm_invoice', views.make_gmmm_invoice, name="make_gmmm_invoice"),
    path('make_reassigned_invoice', views.make_reassigned_invoice, name="make_reassigned_invoice"),
    path('update_r_invoice/<int:pk>', views.update_r_invoice, name="update_r_invoice"),
    path('update_problem_invoice/<int:pk>', views.update_problem_invoice, name="update_problem_invoice"),
    path('update_processed_paid/<int:pk>', views.update_processed_paid, name="update_processed_paid"),
    path('delete_r_invoice/<int:pk>', views.delete_r_invoice, name="delete_r_invoice"),
    path('delete_problem_invoice/<int:pk>', views.delete_problem_invoice, name="delete_problem_invoice"),
    path('invoice_status/<int:pk>', views.invoice_status, name="invoice_status"),

    path('added_status/<int:pk>', views.added_status, name="added_status"),
    path('added_paid_status/<int:pk>', views.added_paid_status, name="added_paid_status"),
    path('added_problem_status/<int:pk>', views.added_problem_status, name="added_problem_status"),
    path('added_reassign_status/<int:pk>', views.added_reassign_status, name="added_reassign_status"),
    path('reassigned_added_status/<int:pk>', views.reassigned_added_status, name="reassigned_added_status"),

    path('completed_status/<int:pk>', views.completed_status, name="completed_status"),
    path('completed_reassigned_status/<int:pk>', views.completed_reassigned_status, name="completed_reassigned_status"),
    path('completed_problem_status/<int:pk>', views.completed_problem_status, name="completed_problem_status"),
    path('completed_denied_status/<int:pk>', views.completed_denied_status, name="completed_denied_status"),
    path('completed_cancelled_status/<int:pk>', views.completed_cancelled_status, name="completed_cancelled_status"),

    path('processed_reassigned_status/<int:pk>', views.processed_reassigned_status, name="processed_reassigned_status"),
    path('denied_status/<int:pk>', views.denied_status, name="denied_status"),
    path('cancelled_status/<int:pk>', views.cancelled_status, name="cancelled_status"),
    path('paid_status/<int:pk>', views.paid_status, name="paid_status"),
    path('paid_reassigned_status/<int:pk>', views.paid_reassigned_status, name="paid_reassigned_status"),
    path('reassigned_paid_status/<int:pk>', views.reassigned_paid_status, name="reassigned_paid_status"),

    path('problem_status/<int:pk>', views.problem_status, name="problem_status"),
    path('problem_invoice_status/<int:pk>', views.problem_invoice_status, name="problem_invoice_status"),
    path('problem_paid_status/<int:pk>', views.problem_paid_status, name="problem_paid_status"),
    path('problem_added_status/<int:pk>', views.problem_added_status, name="problem_added_status"),
    path('problem_completed_status/<int:pk>', views.problem_completed_status, name="problem_completed_status"),
    path('problem_denied_status/<int:pk>', views.problem_denied_status, name="problem_denied_status"),
    path('problem_cancelled_status/<int:pk>', views.problem_cancelled_status, name="problem_cancelled_status"),
    path('problem_reassigned_status/<int:pk>', views.problem_reassigned_status, name="problem_reassigned_status"),

    path('problem_inv_status/<int:pk>', views.problem_inv_status, name="problem_inv_status"),
    path('rely_invoice_processed', views.rely_invoice_processed, name="rely_invoice_processed"),
    path('rely_invoice_completed', views.rely_invoice_completed, name="rely_invoice_completed"),
    path('rely_invoice_paid', views.rely_invoice_paid, name="rely_invoice_paid"),
    path('rely_invoice_problem', views.rely_invoice_problem, name="rely_invoice_problem"),
    path('rely_invoice_reassign', views.rely_invoice_reassign, name="rely_invoice_reassign"),


    path('move_dispatches', views.move_dispatches, name='move_dispatches'),



]
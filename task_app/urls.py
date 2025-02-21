from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name="index"),
    path('add_task', views.add_task, name="add_task"),
    path('update_task/<int:pk>', views.update_task, name="update_task"),  
    path('journal', views.thread, name="journal"),
    path('invoices', views.invoices, name="invoices"),
    path('create_invoice', views.create_invoice, name="create_invoice"),
    path('update_invoice/<int:pk>', views.update_invoice, name="update_invoice"),
]

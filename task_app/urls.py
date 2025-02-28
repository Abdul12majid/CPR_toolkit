from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name="index"),
    path('add_task', views.add_task, name="add_task"),
    path('belle_task', views.belle_task, name="belle_task"),
    path('marvin_task', views.marvin_task, name="marvin_task"),
    path('update_task/<int:pk>', views.update_task, name="update_task"),
    path('update_belle_task/<int:pk>', views.update_belle_task, name="update_belle_task"),  
    path('update_marvin_task/<int:pk>', views.update_marvin_task, name="update_marvin_task"),  
    path('complete_task/<int:pk>', views.complete_task, name="complete_task"),
    path('complete_belle_task/<int:pk>', views.complete_belle_task, name="complete_belle_task"),
    path('complete_marvin_task/<int:pk>', views.complete_marvin_task, name="complete_marvin_task"),
    path('journal', views.thread, name="journal"),
    path('invoices', views.invoices, name="invoices"),
    path('create_invoice', views.create_invoice, name="create_invoice"),
    path('update_invoice/<int:pk>', views.update_invoice, name="update_invoice"),
    path('delete_invoice/<int:pk>', views.delete_invoice, name="delete_invoice"),
    path('add_journal', views.add_journal, name="add_journal"),
    path('login', views.login_user, name="login"),
    path('logout', views.logout_user, name="logout"),
]

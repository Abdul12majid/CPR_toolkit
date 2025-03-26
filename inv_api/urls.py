from . import views
from django.urls import path

urlpatterns = [
    path('create_invoice', views.create_invoice_api, name="create_invoice_api"),
    path('create_ebay', views.create_ebay_api, name="create_ebay_api"),
    path('create_rely_invoice', views.create_rely_invoice, name="create_rely_invoice"),
    path('create_task_api', views.create_task_api, name="create_task_api"),
    path('belle_task_api', views.belle_task_api, name="belle_task_api"),
    path('today_order_api', views.today_order_api, name="today_order_api"),
    path('work_order_api', views.work_order_api, name="work_order_api"),

]
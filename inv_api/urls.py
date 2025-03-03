from . import views
from django.urls import path

urlpatterns = [
    path('create_invoice', views.create_invoice, name="create_invoice"),

]
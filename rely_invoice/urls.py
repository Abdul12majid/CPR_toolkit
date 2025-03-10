from . import views
from django.urls import path

urlpatterns = [
    path('rely_invoice', views.rely_invoice, name="rely_invoice"),

]
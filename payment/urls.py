from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='payment_home'),
    path('events/', views.calendar_events, name='calendar_events'),
    path('events/create/', views.create_event, name='create_event'),
    path('events/update/<int:event_id>/', views.update_event, name='update_event'),
    path('events/delete/<int:event_id>/', views.delete_event, name='delete_event'),

    path('new_student/', views.new_student, name='new_student'),
    path('add_money/', views.add_money, name='add_money'),
    path('deduct_money/', views.deduct_money, name='deduct_money'),
]
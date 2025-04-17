from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import CalendarEvent, Student, Schedule_App_Member
import json
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from datetime import datetime
import logging
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from django.contrib import messages
from decimal import Decimal


@login_required(login_url='login')
def index(request):
    users = User.objects.all()
    students = Student.objects.all()
    sam_students = Student.objects.filter(owner__username="Sam")
    sergio_students = Student.objects.filter(owner__username="Sergio")

    s_app_users = Schedule_App_Member.objects.all()
    sam = Schedule_App_Member.objects.get(first_name="Sam")
    bojan = Schedule_App_Member.objects.get(first_name="Bojan")
    sergio = Schedule_App_Member.objects.get(first_name="Sergio")

    context = {
        "users": users,
        "students": students,
        'sam_students':sam_students,
        'sergio_students':sergio_students,

        "s_app_users": s_app_users,
        "sam": sam,
        "bojan": bojan,
        'sergio':sergio,
    }
    return render(request, 'payment/index.html', context)


@login_required(login_url='login')
def add_money(request):
    if request.method == "POST":
        amount = request.POST.get("amount")
        owner_id = request.POST.get("owner")

        try:
            amount = Decimal(amount)
        except (TypeError, ValueError):
            messages.error(request, "Invalid amount.")
            return redirect("payment_home")

        owner = get_object_or_404(Schedule_App_Member, id=owner_id)
        owner.total_amount += amount
        owner.save()

        messages.success(request, f"Successfully added {amount} to {owner.first_name}")
        return redirect(request.META.get("HTTP_REFERER"))

@login_required(login_url='login')
def deduct_money(request):
    if request.method == "POST":
        amount = request.POST.get("amount")
        owner_id = request.POST.get("owner")

        try:
            amount = Decimal(amount)
        except (TypeError, ValueError):
            messages.error(request, "Invalid amount.")
            return redirect(request.META.get("HTTP_REFERER"))

        owner = get_object_or_404(Schedule_App_Member, id=owner_id)
        owner.total_amount -= amount
        owner.save()

        messages.success(request, f"Successfully deducted {amount} from {owner.first_name}")
        return redirect(request.META.get("HTTP_REFERER"))

@login_required(login_url='login')
def new_student(request):
    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        hourly_rate = request.POST["hourly_rate"]
        first_field = request.POST["google_meet"]
        second_field = request.POST["second_field"]
        owner_id = request.POST["owner"]
        
        owner = User.objects.get(id=owner_id)
        new_student = Student.objects.create(
            first_name=first_name,
            last_name=last_name,
            hourly_rate=hourly_rate,
            first_field=first_field,
            second_field=second_field,
            owner=owner
        )
        new_student.save()
        return redirect("payment_home")
    
    # Get all users for the dropdown, but filter if current user is Sam
    if request.user.username == "Sam":
        users = User.objects.filter(username="Sam")
    else:
        users = User.objects.all()

    sam_students = Student.objects.filter(owner__username="Sam")
    sergio_students = Student.objects.filter(owner__username="Sergio")
    context = {
        "users":users,
        'sam_students':sam_students,
        'sergio_students':sergio_students
    }
    
    return render(request, 'payment/new_student.html', context)


@login_required(login_url='login')
def calendar_events(request):
    # Check if user is Bojan or Sergio - show all events
    if request.user.username in ["Bojan", "Sergio", "spleecho"]:
        events = CalendarEvent.objects.all()
    else:
        # For other users, show events where they're participants
        events = CalendarEvent.objects.filter(participants=request.user)
    
    data = []
    for event in events:
        data.append({
            'id': event.id,
            'title': event.title,
            'start': event.start.isoformat(),
            'end': event.end.isoformat() if event.end else None,
            'allDay': event.all_day,
            'participants': [user.username for user in event.participants.all()],
            'creator': event.creator.username
        })
    return JsonResponse(data, safe=False)

logger = logging.getLogger(__name__)


@require_http_methods(["POST"])
@login_required
def create_event(request):
    try:
        data = json.loads(request.body)
        
        # Validate required fields
        if not data.get('title') or not data.get('start'):
            return JsonResponse(
                {'status': 'error', 'message': 'Title and start time are required'},
                status=400
            )

        # Parse datetimes
        try:
            start = timezone.make_aware(datetime.fromisoformat(data['start']))
            end = timezone.make_aware(datetime.fromisoformat(data['end'])) if data.get('end') else None
        except ValueError as e:
            return JsonResponse(
                {'status': 'error', 'message': f'Invalid date format: {str(e)}'},
                status=400
            )

        # Create all events (original + repeats if needed)
        events = []
        main_event = CalendarEvent(
            title=data['title'],
            start=start,
            end=end,
            all_day=data.get('allDay', False),
            creator=request.user,
            is_recurring=data.get('isRecurring', False),
            recurrence_frequency=data.get('recurrenceFrequency')
        )
        main_event.save()
        events.append(main_event)

        # Create recurring events if needed
        if data.get('isRecurring') and data.get('recurrenceFrequency'):
            frequency = data['recurrenceFrequency']
            for i in range(1, 5):  # Create 4 more events (total 5)
                new_start = start
                new_end = end
                
                if frequency == 'daily':
                    new_start = start + timedelta(days=i)
                    if end:
                        new_end = end + timedelta(days=i)
                elif frequency == 'weekly':
                    new_start = start + timedelta(weeks=i)
                    if end:
                        new_end = end + timedelta(weeks=i)
                elif frequency == 'monthly':
                    new_start = start + relativedelta(months=+i)
                    if end:
                        new_end = end + relativedelta(months=+i)
                
                recurring_event = CalendarEvent(
                    title=data['title'],
                    start=new_start,
                    end=new_end,
                    all_day=data.get('allDay', False),
                    creator=request.user,
                    is_recurring=True,
                    recurrence_frequency=frequency
                )
                recurring_event.save()
                events.append(recurring_event)

        # Add participants to all events
        participants = data.get('participants', [])
        if participants:
            participant_users = User.objects.filter(username__in=participants)
            for event in events:
                event.participants.add(*participant_users)

        return JsonResponse({
            'status': 'success',
            'event': {
                'id': main_event.id,
                'title': main_event.title,
                'start': main_event.start.isoformat(),
                'end': main_event.end.isoformat() if main_event.end else None,
                'allDay': main_event.all_day,
                'participants': [user.username for user in main_event.participants.all()],
                'creator': main_event.creator.username,
                'isRecurring': main_event.is_recurring,
                'recurrenceFrequency': main_event.recurrence_frequency
            }
        })

    except Exception as e:
        return JsonResponse(
            {'status': 'error', 'message': str(e)},
            status=400
        )


@require_http_methods(["PUT"])
@login_required(login_url='login')
def update_event(request, event_id):
    try:
        logger.info(f"Update event request received for event {event_id}")
        data = json.loads(request.body)
        logger.debug(f"Request data: {data}")
        
        # Get event - no longer checking creator
        logger.debug(f"Looking for event {event_id}")
        event = CalendarEvent.objects.get(id=event_id)

        # Log current values
        logger.debug(f"Current values - Title: {event.title}, Start: {event.start}, End: {event.end}, AllDay: {event.all_day}")
        
        # Update fields
        if 'title' in data:
            event.title = data['title']
            logger.debug(f"Updating title to: {data['title']}")
        
        if 'start' in data:
            new_start = timezone.make_aware(datetime.fromisoformat(data['start']))
            logger.debug(f"Updating start from {event.start} to {new_start}")
            event.start = new_start
        
        if 'end' in data:
            new_end = timezone.make_aware(datetime.fromisoformat(data['end'])) if data['end'] else None
            logger.debug(f"Updating end from {event.end} to {new_end}")
            event.end = new_end
        
        if 'allDay' in data:
            logger.debug(f"Updating allDay from {event.all_day} to {data['allDay']}")
            event.all_day = data['allDay']
        
        event.save()
        logger.debug("Event saved successfully")

        # Update participants if provided
        if 'participants' in data:
            logger.debug(f"Updating participants to: {data['participants']}")
            event.participants.clear()
            if data['participants']:
                participant_users = User.objects.filter(username__in=data['participants'])
                event.participants.add(*participant_users)

        response_data = {
            'status': 'success',
            'event': {
                'id': event.id,
                'title': event.title,
                'start': event.start.isoformat(),
                'end': event.end.isoformat() if event.end else None,
                'allDay': event.all_day,
                'participants': [user.username for user in event.participants.all()],
                'creator': event.creator.username
            }
        }
        
        logger.info(f"Event {event_id} updated successfully")
        logger.debug(f"Response data: {response_data}")
        return JsonResponse(response_data)

    except CalendarEvent.DoesNotExist:
        logger.error(f"Event not found: {event_id}")
        return JsonResponse(
            {'status': 'error', 'message': 'Event not found'},
            status=404
        )
    except Exception as e:
        logger.error(f"Error updating event {event_id}: {str(e)}", exc_info=True)
        return JsonResponse(
            {'status': 'error', 'message': str(e)},
            status=400
        )
@require_http_methods(["DELETE"])
@login_required
def delete_event(request, event_id):
    try:
        logger.info(f"Delete event request received for event {event_id}")
        
        # Get event - no creator check since anyone can delete
        event = CalendarEvent.objects.get(id=event_id)
        event.delete()
        
        logger.info(f"Event {event_id} deleted successfully")
        return JsonResponse({'status': 'success'})

    except CalendarEvent.DoesNotExist:
        logger.error(f"Event not found: {event_id}")
        return JsonResponse(
            {'status': 'error', 'message': 'Event not found'},
            status=404
        )
    except Exception as e:
        logger.error(f"Error deleting event {event_id}: {str(e)}", exc_info=True)
        return JsonResponse(
            {'status': 'error', 'message': str(e)},
            status=400
        )
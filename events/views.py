from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import Http404
from django.contrib import messages
from django.shortcuts import redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from .models import Event
from .forms import EventForm, SearchForm

from datetime import datetime

def home(request):
    show_old = False
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            search = form.cleaned_data.get('search')
            show_old = form.cleaned_data.get('show_old')
            events = Event.objects.filter(Q(name__icontains=search)|Q(details__icontains=search))
        else:
            messages.warning(request,'Something went wrong!')
            events = Event.objects.all()
            # then call to render below
    else:
        events = Event.objects.all()
        form = SearchForm()
    if not show_old:
        events = events.filter(event_date__gt=datetime.now())
    events = events.order_by('event_date')
    return render(request, 'home.html',{'events':events, 'form':form})

def event_detail(request, id):
    try:
        event = Event.objects.get(id=id)
    except Event.DoesNotExist:
        raise Http404('Event does\'t exist')
    return render(request, 'event_detail.html',{'event':event})

def create_event(request):
    if not request.user.is_authenticated: # if user is not logged in
        # Unlike the @login_required decorator, this displays a friendly error message
        messages.warning(request,'You must be logged in to create an event')
        return redirect('login')
    if request.method == 'POST': # if request is submitting form data
        filled_form = EventForm(request.POST)
        if filled_form.is_valid():
            filled_form.instance.author = request.user # fill in author with current user
            filled_form.save()
            filled_form.instance.signed_up.add(request.user)

            eventName = filled_form.cleaned_data.get('name')
            messages.success(request,f'{eventName} has been created!')
            return redirect('home')
        else:
            messages.warning(request,'Something went wrong!')
            return render(request,'create_event.html',{'form':filled_form})
    else: # If logged in user is accessing the page through a normal GET request
        form = EventForm()
        return render(request, 'create_event.html',{'form':form})

def edit_event(request, id):

    try:
        event = Event.objects.get(id=id)

    except Event.DoesNotExist:
        raise Http404('Event does\'t exist')
    form =EventForm( instance =event)
    if request.method == 'POST':
        form = EventForm( request.POST, instance =event)
        if form.is_valid():
            form.save()
            messages.success(request,f'Changes have been made to your event')
            return redirect('event detail',id)
        else:
            messages.warning(request,'Something is wrong with your form')
            return render(request, 'create_event.html', {'form' : form})

    return render(request, 'create_event.html', {'form': form})

@login_required
def signup(request, event_id):
    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        raise Http404('Event does\'t exist')
    event.signed_up.add(request.user)
    event.save()
    messages.success(request,f'Signed up for { event.name }')
    return redirect('home')

@login_required
def cancel_signup(request, event_id):
    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        raise Http404('Event does\'t exist')
    event.signed_up.remove(request.user)
    event.save()
    messages.success(request,f'Canceled on { event.name }')
    return redirect('home')

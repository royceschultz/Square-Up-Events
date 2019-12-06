from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import Http404
from django.contrib import messages
from django.shortcuts import redirect
from django.db.models import Q, Count
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe

from .models import Event
from .forms import EventForm, SearchForm

from datetime import datetime

def home(request):
    events = Event.objects.all()
    form = SearchForm(request.GET)
    search = request.GET.get('search')
    if search:
        events = events.filter(Q(name__icontains=search)|Q(details__icontains=search))
    show_old = request.GET.get('show_old')
    if not show_old:
        events = events.filter(event_date__gt=datetime.now())
    #sorting events
    sort_by = request.GET.get('sort')
    if sort_by is not None and sort_by != '':
        sort_by = int(sort_by)
    events = events.order_by('event_date')
    if sort_by == 1:
        events = events.annotate(count=Count('signed_up')).order_by('-count', 'event_date')
    elif sort_by == 2:
        events = events.annotate(count=Count('signed_up')).order_by('count', 'event_date')
    elif sort_by == 3:
        events = events.order_by('event_date')
    elif sort_by == 4:
        events = events.order_by('-create_date')

    #category filter
    categories = request.GET.getlist('category')
    if categories:
        events = events.filter(category__in=categories)

    return render(request, 'home.html',{'events':events,'sort_by':sort_by,'form':form})

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

            event = filled_form.instance
            message = f'<a href="event/{event.id}"> {event.name} </a> has been created!'
            messages.success(request, mark_safe(message))
            return redirect('home')
        else:
            messages.warning(request,'Something went wrong!')
            return render(request,'create_event.html',{'form':filled_form})
    else: # If logged in user is accessing the page through a normal GET request
        form = EventForm()
        return render(request, 'create_event.html',{'form':form})

@login_required
def edit_event(request, id):


    try:
        event = Event.objects.get(id=id)

    except Event.DoesNotExist:
        raise Http404('Event does\'t exist')

    if(event.author == request.user):
        form =EventForm( instance =event)
        if request.method == 'POST':
            form = EventForm( request.POST, instance =event)
            if form.is_valid():
                form.save()
                message = f'Changes have been made to <a href="event/{event.id}"> {event.name} </a>'
                messages.success(request,mark_safe(message))
                return redirect('event detail',id)
            else:
                messages.warning(request,'Something is wrong with your form')
                return render(request, 'create_event.html', {'form' : form})

        return render(request, 'create_event.html', {'form': form})
    else:
        messages.warning(request,'You do not have permission to edit this')
        return redirect('home')



@login_required
def signup(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        try:
            event = Event.objects.get(id=id)
        except Event.DoesNotExist:
            raise Http404('Event does\'t exist')
        if request.POST.get('signed_up'):
            event.signed_up.remove(request.user)
            message = f'Canceled on <a href="event/{event.id}"> {event.name} </a>'
        else:
            event.signed_up.add(request.user)
            message = f'Signed up for <a href="event/{event.id}"> {event.name} </a>'
        event.save()
        messages.success(request,mark_safe(message))
        return redirect('home')
    return redirect('home')

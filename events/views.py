from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from django.contrib import messages

from .models import Event
from .forms import EventForm

def home(request):
    events = Event.objects.all()
    return render(request, 'home.html',{'events':events})

def event_detail(request, id):
    try:
        event = Event.objects.get(id=id)
    except Room.DoesNotExist:
        raise Http404('room not found')
    return render(request, 'event_detail.html',{'event':event})

def create_event(request):
    if request.method == 'POST':
        filled_form = EventForm(request.POST)
        if filled_form.is_valid():
            filled_form.save()
            eventName = filled_form.cleaned_data.get('name')
            messages.success(request,f'{eventName} has been created!')
            return render(request,'home.html')
        else:
            messages.warning(request,'Something went wrong!')
            return render(request,'create_event.html',{'form':filled_form})
    else:
        form = EventForm()
        return render(request, 'create_event.html',{'form':form})


# Create your views here.

from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404

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
            note = 'Event Created'
            new_form = EventForm()
            return render(request,'create_event.html',{'form':new_form,'note':note})
        else:
            note = 'there\'s an error'
            return render(request,'create_event.html',{'form':filled_form,'note':note})
    else:
        form = EventForm()
        return render(request, 'create_event.html',{'form':form})


# Create your views here.

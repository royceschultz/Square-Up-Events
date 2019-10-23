from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ['author'] # author will be determined by request.user
        labels = {
            'event_date': 'Datetime of event (format: MM/DD/YYYY 24H:MM)'
        }
        widgets = {
            'event_date': forms.Textarea(attrs={'cols': 80, 'rows': 3}), # TODO: replace with datetime widget
        }

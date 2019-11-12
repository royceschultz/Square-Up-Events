from django import forms
from .models import Event
from .widgets import BootstrapDateTimePickerInput

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ['author','signed_up'] # author will be determined by request.user
        labels = {
            'event_date': 'Date and time of event (format: MM/DD/YYYY 24H:MM)'
        }
        widgets = {
            'event_date': BootstrapDateTimePickerInput()
        }

class SearchForm(forms.Form):
    search = forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder': 'search for events'}),max_length=100, required=False)
    show_old = forms.BooleanField(label='show old events', required=False)

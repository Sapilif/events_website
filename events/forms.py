from django import forms
from django.forms import ModelForm
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import Ticket, Event


class EventForm(ModelForm):
	hour = forms.ChoiceField(

        choices=[("12:00", "12:00"), ("13:00", "13:00"), ("14:00", "14:00"), ("15:00", "15:00"), 
        ("16:00", "16:00"), ("17:00", "17:00"), ("18:00", "18:00"), ("19:00", "19:00"), 
        ("20:00", "20:00"), ("21:00", "21:00"), ("22:00", "22:00"), ("23:00", "23:00"), 
        ("00:00", "00:00"), ("01:00", "01:00"), ("02:00", "02:00"), ("03:00", "03:00"), 
        ("04:00", "04:00"), ("05:00", "05:00"), ("06:00", "06:00"), ("07:00", "07:00"), 
        ("08:00", "08:00"), ("09:00", "09:00"), ("10:00", "10:00"), ("11:00", "11:00")],
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Selectati ora evenimentului',
        )
	class Meta:
		model = Event
		fields = ('name', 'description', 'location', 'eveniment_image', 'eveniment_date','tickets', 'ticket_price')

		labels = {
			'name': 'Introduceti numele evenimentului:',
			'description': 'Introduceti descrierea evenimentului:',
			'location': 'Introduceti locatia evenimentului:',
			'eveniment_image': 'Adauga o imagine pentru eveniment:',
			'eveniment_date': 'Selecteaza data evenimentului:',
			'tickets': 'Introduceti numarul de bilete disponibile:',
			'ticket_price': 'Introduceti pretul unui bilet:',
		}

		widgets = {
			'name': forms.TextInput(attrs={'class':'form-control'}),
			'description': forms.Textarea(attrs={'class':'form-control'}),
			'location': forms.TextInput(attrs={'class':'form-control'}),
			'eveniment_date': forms.SelectDateWidget(attrs={'class':'form-select'}),
			'tickets': forms.TextInput(attrs={'class':'form-select'}),
			'ticket_price': forms.TextInput(attrs={'class':'form-control'}),
		}

    


class TicketForm(ModelForm):
	number_of_tickets = forms.ChoiceField(
        choices=[(str(i), str(i)) for i in range(1, 6)],
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Numarul de bilete pe care doriti sa le achizitionati',
    )
	class Meta:
		model = Ticket
		fields = ('nume', 'prenume')

		labels = {
			'nume': '',
			'prenume': '',
		}

		widgets = {
			'nume': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nume'}),
			'prenume': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Prenume'}),
		}

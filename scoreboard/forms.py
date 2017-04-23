from django import forms
from django.contrib.admin.widgets import AdminDateWidget

from .models import Sport, Event, Team


class SportForm(forms.ModelForm):
	class Meta:
		model = Sport
		exclude = ('creator', )
		labels = {'name': 'Nome'}

	def __init__(self, *args, **kwargs):
		super(SportForm, self).__init__(*args, **kwargs)
		labels_to_placeholder(self.fields)


class EventForm(forms.ModelForm):
	class Meta:
		model = Event
		exclude = ('sport', 'score0', 'score1', 'expired')
		labels = {'team0': 'Prima squadra:',
		          'team1': 'Seconda squadra',
		          'match_date': 'Data'}
		widgets = {'match_date': AdminDateWidget()}  # todo fix

	def __init__(self, *args, **kwargs):
		sport = kwargs.pop('sport')
		super(EventForm, self).__init__(*args, **kwargs)
		self.fields["team0"].queryset = self.fields["team1"].queryset = Team.objects.filter(sport=sport)
		self.fields['match_date'].widget.attrs['placeholder'] = 'DD-MM-YYYY HH:MM'

	def clean(self):
		cleaned_data = super(EventForm, self).clean()
		if cleaned_data['team0'] == cleaned_data['team1']:
			raise forms.ValidationError('Partita non valida.')
		return cleaned_data


class TeamForm(forms.ModelForm):
	class Meta:
		model = Team
		exclude = ('sport', 'score')
		labels = {'name': 'Nome'}

	def __init__(self, *args, **kwargs):
		super(TeamForm, self).__init__(*args, **kwargs)
		labels_to_placeholder(self.fields)


def labels_to_placeholder(fields):
	for field in fields:
		fields[field].widget.attrs['placeholder'] = fields[field].label

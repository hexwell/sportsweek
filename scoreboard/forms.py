from django import forms

from .models import Sport


class SportForm(forms.ModelForm):
	class Meta:
		model = Sport
		exclude = ('creator', )
		labels = {'name': 'Nome'}

	def __init__(self, *args, **kwargs):
		super(SportForm, self).__init__(*args, **kwargs)
		self.fields['name'].widget.attrs['placeholder'] = self.fields['name'].label

from django import forms

from .models import Sport


class SportForm(forms.ModelForm):
	class Meta:
		model = Sport
		fields = ['name']

	def clean(self):
		cleaned_data = super(SportForm, self).clean()
		
		return cleaned_data

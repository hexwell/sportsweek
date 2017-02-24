from django.views import generic

from .models import Sport


class IndexView(generic.ListView):
	model = Sport
	context_object_name = 'sports'
	template_name = 'scoreboard/index.html'

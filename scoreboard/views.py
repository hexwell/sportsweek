from django.shortcuts import render
from django.views import generic

from .models import Sport, Team


class IndexView(generic.ListView):
	model = Sport
	context_object_name = 'sports'
	template_name = 'scoreboard/index.html'


def ranking_view(request, sport_name):
	context = {
		'teams': Team.objects.filter(sport=Sport.objects.filter(name=sport_name)).order_by('-score')
	}
	return render(request, 'scoreboard/ranking.html', context)

import datetime

from django.shortcuts import render, get_object_or_404
from django.views import generic

from .models import Sport, Team, Event


class IndexView(generic.ListView):
	model = Sport
	context_object_name = 'sports'
	template_name = 'scoreboard/index.html'


def ranking_view(request, sport_name):
	get_object_or_404(Sport.objects.filter(name=sport_name))
	context = {
		'sport_name': sport_name,
		'teams': Team.objects.filter(sport=Sport.objects.filter(name=sport_name)).order_by('-score')
	}
	events = []
	for event in Event.objects.filter(sport__name=sport_name).order_by('-match_date'):
		if not event.expired and event.is_imminent(datetime.timedelta(minutes=30)):
			events.append(event)
	if events:
		context['events'] = events

	return render(request, 'scoreboard/ranking.html', context)

import datetime

from django.shortcuts import render, get_object_or_404
from django.views import generic

from .models import Sport, Team, Event

interval = datetime.timedelta(minutes=30)


class IndexView(generic.ListView):
	model = Sport
	context_object_name = 'sports'
	template_name = 'scoreboard/index.html'


def ranking_view(request, sport_id):
	sport_obj = get_object_or_404(Sport.objects.filter(id=sport_id))
	context = {
		'sport_name': sport_obj.name,
		'teams': Team.objects.filter(sport=sport_obj).order_by('-score')
	}
	events = []
	for event in Event.objects.filter(sport=sport_obj).order_by('-match_date'):
		if event.can_be_shown(interval):
			events.append(event)
	if events:
		context['events'] = events

	return render(request, 'scoreboard/ranking.html', context)

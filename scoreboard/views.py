import datetime

from django.shortcuts import get_object_or_404
from django.http import HttpResponseBadRequest, JsonResponse
from django.views.generic import ListView

from .models import Sport, Team, Event

interval = datetime.timedelta(minutes=30)


class IndexView(ListView):
	model = Sport
	context_object_name = 'sports'
	template_name = 'scoreboard/index.html'


class RankingList(ListView):
	model = Team
	template_name = 'scoreboard/ranking.html'
	context_object_name = 'teams'
	sport_obj = None

	def get_queryset(self):
		self.sport_obj = get_object_or_404(Sport.objects.filter(id=self.kwargs.get('sport_id', '')))
		return Team.objects.filter(sport=self.sport_obj).order_by('-score')

	def get_context_data(self, **kwargs):
		context = super(RankingList, self).get_context_data(**kwargs)
		context['sport_name'] = self.sport_obj.name
		events = []
		for event in Event.objects.filter(sport=self.sport_obj).order_by('-match_date'):
			if event.can_be_shown(interval):
				events.append(event)
		if events:
			context['events'] = events
		return context


def get_updated_scores(request):
	ids = request.GET.get('ids', False)
	if not ids:
		return HttpResponseBadRequest(request)

	events = {get_object_or_404(Event.objects.filter(id=id_)) for id_ in ids.split('.')}

	data = {event.id: {"score0": event.score0, "score1": event.score1} for event in events}
	return JsonResponse(data)

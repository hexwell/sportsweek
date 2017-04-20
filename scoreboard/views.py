import datetime

from django.shortcuts import get_object_or_404, reverse
from django.http import HttpResponseBadRequest, JsonResponse
from django.views.generic import ListView, FormView
from django.forms.utils import ErrorList
from django.forms import forms as forms_
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import Sport, Team, Event
from .forms import SportForm

interval = datetime.timedelta(minutes=30)


class IndexView(ListView):
	model = Sport
	context_object_name = 'sports'
	template_name = 'scoreboard/index.html'

	def get_context_data(self, **kwargs):
		context = super(IndexView, self).get_context_data(**kwargs)
		context['has_permission'] = create_sport_permission_check(self.request.user)
		return context


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


class SportFormView(LoginRequiredMixin, UserPassesTestMixin, FormView):
	template_name = 'scoreboard/create_sport.html'
	form_class = SportForm

	def test_func(self):
		return create_sport_permission_check(self.request.user, bypass_admin=True)

	def get_login_url(self):
		if not self.request.user.is_authenticated():
			return super(SportFormView, self).get_login_url()
		else:
			return reverse('scoreboard:index')

	def get_success_url(self):
		return reverse('scoreboard:index')

	def form_valid(self, form):
		if not create_sport_permission_check(self.request.user, bypass_admin=True):
			errors = form.errors.setdefault(forms_.NON_FIELD_ERRORS, ErrorList())
			errors.append("User already created a sport")
			return self.form_invalid(form)
		form.instance.creator = self.request.user
		form.save()
		return super(SportFormView, self).form_valid(form)


def create_sport_permission_check(user, bypass_admin=False):
	if user.is_authenticated:
		is_sport_adm = len(user.groups.filter(name='Sport_ADM')) == 1
		has_permission = len(Sport.objects.filter(creator=user)) == 0 and is_sport_adm
	else:
		has_permission = False

	if user.is_superuser and not bypass_admin:
		has_permission = True

	return has_permission


def get_updated_scores(request):
	ids = request.GET.get('ids', False)
	if not ids:
		return HttpResponseBadRequest(request)

	events = {get_object_or_404(Event.objects.filter(id=id_)) for id_ in ids.split('.')}

	data = {event.id: {"score0": event.score0, "score1": event.score1} for event in events}
	return JsonResponse(data)

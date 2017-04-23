import datetime

from django.shortcuts import get_object_or_404, reverse
from django.http import HttpResponseBadRequest, JsonResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.forms.utils import ErrorList
from django.forms import forms as forms_
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import Sport, Team, Event
from .forms import SportForm, TeamForm, EventForm

interval = datetime.timedelta(minutes=30)


class IndexView(ListView):
	model = Sport
	context_object_name = 'sports'

	def get_context_data(self, **kwargs):
		context = super(IndexView, self).get_context_data(**kwargs)
		context['has_permission'] = create_sport_permission_check(self.request.user, bypass_admin=False)
		return context


class RankingList(ListView):
	model = Team
	context_object_name = 'teams'
	sport_obj = None

	def get_queryset(self):
		self.sport_obj = get_sport(self.kwargs.get('sport_id'))
		return Team.objects.filter(sport=self.sport_obj).order_by('-score')

	def get_context_data(self, **kwargs):
		context = super(RankingList, self).get_context_data(**kwargs)

		context['sport_name'] = self.sport_obj.name
		context['sport_id'] = self.kwargs.get('sport_id')
		context['sport_ADM'] = edit_sport_permission_check(self.request.user, self.sport_obj)

		events = []
		for event in Event.objects.filter(sport=self.sport_obj).order_by('-match_date'):
			if event.can_be_shown(interval):
				events.append(event)
		if events:
			context['events'] = events

		return context


class EventsList(ListView):
	model = Event
	context_object_name = 'events'
	sport_obj = None

	def get_queryset(self):
		self.sport_obj = get_sport(self.kwargs.get('sport_id'))
		return Event.objects.filter(sport=self.sport_obj).order_by('-match_date')

	def get_context_data(self, **kwargs):
		context = super(EventsList, self).get_context_data(**kwargs)

		events = [[], [], []]

		for event in context.pop('events'):
			if event.can_be_shown(interval=interval):
				events[1].append(event)
				continue
			if event.is_future(interval=interval):
				events[0].append(event)
				continue
			if event.is_past():
				events[2].append(event)

		context['future_events'], context['current_events'], context['past_events'] = events[0], events[1], events[2]
		context['sport_id'] = self.kwargs.get('sport_id')
		context['sport_ADM'] = edit_sport_permission_check(self.request.user, self.sport_obj)

		return context


class CreateSportView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
	model = Sport
	form_class = SportForm

	def test_func(self):
		return create_sport_permission_check(self.request.user, bypass_admin=False)

	def get_login_url(self):
		if not self.request.user.is_authenticated():
			return super(CreateSportView, self).get_login_url()
		else:
			return reverse('scoreboard:index')

	def get_success_url(self):
		return reverse('scoreboard:index')

	def get_context_data(self, **kwargs):
		context = super(CreateSportView, self).get_context_data(**kwargs)
		context['op'] = 'Crea'
		context['next'] = reverse('scoreboard:index')
		return context

	def form_valid(self, form):
		if not create_sport_permission_check(self.request.user):
			errors = form.errors.setdefault(forms_.NON_FIELD_ERRORS, ErrorList())
			errors.append("L'utente ha già creato uno sport")
			return self.form_invalid(form)
		form.instance.creator = self.request.user
		return super(CreateSportView, self).form_valid(form)


class UpdateSportView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Sport
	form_class = SportForm
	template_name_suffix = '_form'

	def test_func(self):
		return edit_sport_permission_check(self.request.user, self.get_object())

	def get_login_url(self):
		if not self.request.user.is_authenticated():
			return super(UpdateSportView, self).get_login_url()
		else:
			return self.request.GET.get('next', reverse('scoreboard:index'))

	def get_success_url(self):
		return self.request.GET.get('next', reverse('scoreboard:index'))

	def get_object(self, queryset=None):
		return get_object_or_404(self.model.objects.filter(id=self.kwargs.get('sport_id')))

	def get_context_data(self, **kwargs):
		context = super(UpdateSportView, self).get_context_data(**kwargs)
		context['op'] = 'Modifica'
		context['next'] = self.request.GET.get('next', reverse('scoreboard:index'))
		return context


class DeleteSportView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Sport

	def test_func(self):
		return edit_sport_permission_check(self.request.user, self.get_object())

	def get_login_url(self):
		if not self.request.user.is_authenticated():
			return super(DeleteSportView, self).get_login_url()
		else:
			return self.request.GET.get('next', reverse('scoreboard:index'))

	def get_success_url(self):
		return reverse('scoreboard:index')

	def get_object(self, queryset=None):
		return get_object_or_404(self.model.objects.filter(id=self.kwargs.get('sport_id')))

	def get_context_data(self, **kwargs):
		context = super(DeleteSportView, self).get_context_data(**kwargs)
		context['next'] = self.request.GET.get('next', reverse('scoreboard:index'))
		return context


class CreateEventView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
	model = Event
	form_class = EventForm

	def test_func(self):
		return edit_sport_permission_check(self.request.user, get_sport(self.kwargs.get('sport_id')))

	def get_login_url(self):
		if not self.request.user.is_authenticated():
			return super(CreateEventView, self).get_login_url()
		else:
			return self.request.GET.get('next', reverse('scoreboard:ranking', args=(self.kwargs['sport_id'],)))

	def get_success_url(self):
		return self.request.GET.get('next', reverse('scoreboard:ranking', args=(self.kwargs['sport_id'],)))

	def get_form_kwargs(self):
		kwargs = super(CreateEventView, self).get_form_kwargs()
		kwargs['sport'] = get_sport(self.kwargs.get('sport_id'))
		return kwargs

	def get_context_data(self, **kwargs):
		context = super(CreateEventView, self).get_context_data(**kwargs)
		context['op'] = 'Crea'
		context['next'] = self.request.GET.get('next', reverse('scoreboard:ranking', args=(self.kwargs['sport_id'],)))
		return context

	def form_valid(self, form):
		form.instance.sport = get_sport(self.kwargs.get('sport_id'))
		return super(CreateEventView, self).form_valid(form)


class UpdateEventView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Event
	form_class = EventForm
	template_name_suffix = '_form'

	def test_func(self):
		return edit_sport_permission_check(self.request.user, get_sport(self.kwargs.get('sport_id')))

	def get_login_url(self):
		if not self.request.user.is_authenticated():
			return super(UpdateEventView, self).get_login_url()
		else:
			return self.request.GET.get('next', reverse('scoreboard:ranking', args=(self.kwargs['sport_id'],)))

	def get_success_url(self):
		return self.request.GET.get('next', reverse('scoreboard:ranking', args=(self.kwargs['sport_id'],)))

	def get_object(self, queryset=None):
		return get_object_or_404(Event.objects.filter(id=self.kwargs.get('event_id')))

	def get_context_data(self, **kwargs):
		context = super(UpdateEventView, self).get_context_data(**kwargs)
		context['op'] = 'Modifica'
		context['next'] = self.request.GET.get('next', reverse('scoreboard:ranking', args=(self.kwargs['sport_id'],)))
		return context

	def get_form_kwargs(self):
		kwargs = super(UpdateEventView, self).get_form_kwargs()
		kwargs['sport'] = get_sport(self.kwargs.get('sport_id'))
		return kwargs


class DeleteEventView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Sport

	def test_func(self):
		return edit_sport_permission_check(self.request.user, get_sport(self.kwargs.get('sport_id')))

	def get_login_url(self):
		if not self.request.user.is_authenticated():
			return super(DeleteEventView, self).get_login_url()
		else:
			return self.request.GET.get('next', reverse('scoreboard:ranking', args=(self.kwargs['sport_id'],)))

	def get_success_url(self):
		return self.request.GET.get('next', reverse('scoreboard:ranking', args=(self.kwargs['sport_id'],)))

	def get_object(self, queryset=None):
		return get_object_or_404(Event.objects.filter(id=self.kwargs.get('event_id')))

	def get_context_data(self, **kwargs):
		context = super(DeleteEventView, self).get_context_data(**kwargs)
		context['next'] = self.request.GET.get('next', reverse('scoreboard:ranking', args=(self.kwargs['sport_id'],)))
		return context


class CreateTeamView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
	model = Team
	form_class = TeamForm

	def test_func(self):
		return edit_sport_permission_check(self.request.user, get_sport(self.kwargs.get('sport_id')))

	def get_login_url(self):
		if not self.request.user.is_authenticated():
			return super(CreateTeamView, self).get_login_url()
		else:
			return reverse('scoreboard:ranking', args=(self.kwargs['sport_id'],))

	def get_success_url(self):
		return reverse('scoreboard:ranking', args=(self.kwargs['sport_id'],))

	def get_context_data(self, **kwargs):
		context = super(CreateTeamView, self).get_context_data(**kwargs)
		context['op'] = 'Crea'
		context['sport_id'] = self.kwargs['sport_id']
		return context

	def form_valid(self, form):
		form.instance.sport = get_sport(self.kwargs.get('sport_id'))
		return super(CreateTeamView, self).form_valid(form)


class UpdateTeamView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Team
	form_class = TeamForm
	template_name_suffix = '_form'

	def test_func(self):
		return edit_sport_permission_check(self.request.user, get_sport(self.kwargs.get('sport_id')))

	def get_login_url(self):
		if not self.request.user.is_authenticated():
			return super(UpdateTeamView, self).get_login_url()
		else:
			return reverse('scoreboard:ranking', args=(self.kwargs['sport_id'],))

	def get_success_url(self):
		return reverse('scoreboard:ranking', args=(self.kwargs['sport_id'],))

	def get_object(self, queryset=None):
		return get_object_or_404(Team.objects.filter(id=self.kwargs.get('team_id')))

	def get_context_data(self, **kwargs):
		context = super(UpdateTeamView, self).get_context_data(**kwargs)
		context['op'] = 'Modifica'
		context['sport_id'] = self.kwargs['sport_id']
		return context


class DeleteTeamView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Team

	def test_func(self):
		return edit_sport_permission_check(self.request.user, get_sport(self.kwargs.get('sport_id')))

	def get_login_url(self):
		if not self.request.user.is_authenticated():
			return super(DeleteTeamView, self).get_login_url()
		else:
			return reverse('scoreboard:ranking', args=(self.kwargs['sport_id'],))

	def get_success_url(self):
		return reverse('scoreboard:ranking', args=(self.kwargs['sport_id'],))

	def get_object(self, queryset=None):
		return get_object_or_404(Team.objects.filter(id=self.kwargs.get('team_id')))


def get_sport(id_):
	return get_object_or_404(Sport.objects.filter(id=id_))


def create_sport_permission_check(user, bypass_admin=True):
	if user.is_authenticated:
		is_sport_adm = len(user.groups.filter(name='Sport_ADM')) == 1
		if len(Sport.objects.filter(creator=user)) == 0 and is_sport_adm:
			return True
		if user.is_superuser and not bypass_admin:
			return True

	return False


def edit_sport_permission_check(user, sport):
	if user.is_authenticated:
		if sport.creator == user:
			return True
		else:
			if user.is_superuser:
				return True

	return False


def get_updated_scores(request):
	ids = request.GET.get('ids', False)
	if not ids:
		return HttpResponseBadRequest(request)

	events = {get_object_or_404(Event.objects.filter(id=id_)) for id_ in ids.split('.')}

	data = {event.id: {"score0": event.score0, "score1": event.score1} for event in events}
	return JsonResponse(data)

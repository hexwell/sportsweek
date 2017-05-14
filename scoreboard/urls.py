from django.conf.urls import url

from . import views

app_name = 'scoreboard'
urlpatterns = [
	url(r'^getupdatedscores/$', views.get_updated_scores, name="get_updated_scores"),
	url(r'^$', views.IndexView.as_view(), name='index'),
	url(r'^(?P<sport_id>[0-9]+)/$', views.RankingList.as_view(), name='ranking'),
	url(r'^(?P<sport_id>[0-9]+)/events/$', views.EventsList.as_view(), name="events"),
	url(r'^(?P<sport_id>[0-9]+)/events/(?P<event_id>[0-9]+)/scores/(?P<team>[0-1])/(?P<val>[+\-])/$',
	    views.update_scores, name="update_scores"),
	url(r'^(?P<sport_id>[0-9]+)/events/create/$', views.CreateEventView.as_view(), name="create_event"),
	url(r'^(?P<sport_id>[0-9]+)/events/(?P<event_id>[0-9]+)/end/$', views.end_event, name="end_event"),
	url(r'^(?P<sport_id>[0-9]+)/events/(?P<event_id>[0-9]+)/update/$',
	    views.UpdateEventView.as_view(), name="update_event"),
	url(r'^(?P<sport_id>[0-9]+)/events/(?P<event_id>[0-9]+)/delete/$',
	    views.DeleteEventView.as_view(), name="delete_event"),
	url(r'^(?P<sport_id>[0-9]+)/teams/create/$', views.CreateTeamView.as_view(), name="create_team"),
	url(r'^(?P<sport_id>[0-9]+)/teams/(?P<team_id>[0-9]+)/update/$',
	    views.UpdateTeamView.as_view(), name="update_team"),
	url(r'^(?P<sport_id>[0-9]+)/teams/(?P<team_id>[0-9]+)/delete/$',
	    views.DeleteTeamView.as_view(), name="delete_team"),
	url(r'^create/sport/$', views.CreateSportView.as_view(), name="create_sport"),
	url(r'^(?P<sport_id>[0-9]+)/update/$', views.UpdateSportView.as_view(), name="update_sport"),
	url(r'^(?P<sport_id>[0-9]+)/delete/$', views.DeleteSportView.as_view(), name="delete_sport"),
]

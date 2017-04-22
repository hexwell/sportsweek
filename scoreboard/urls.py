from django.conf.urls import url

from . import views

app_name = 'scoreboard'
urlpatterns = [
	url(r'^getupdatedscores/$', views.get_updated_scores, name="get_updated_scores"),
	url(r'^$', views.IndexView.as_view(), name='index'),
	url(r'^(?P<sport_id>[0-9]+)/$', views.RankingList.as_view(), name='ranking'),
	url(r'^(?P<sport_id>[0-9]+)/create/event/$', views.CreateSportView.as_view(), name="create_event"),
	url(r'^create/sport/$', views.CreateSportView.as_view(), name="create_sport"),
	url(r'^(?P<sport_id>[0-9]+)/update/$', views.UpdateSportView.as_view(), name="update_sport"),
	url(r'^(?P<sport_id>[0-9]+)/delete/$', views.DeleteSportView.as_view(), name="delete_sport"),
]

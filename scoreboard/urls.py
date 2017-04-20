from django.conf.urls import url

from . import views

app_name = 'scoreboard'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<sport_id>[0-9]+)/$', views.RankingList.as_view(), name='ranking'),
    url(r'^getupdatedscores/$', views.get_updated_scores, name="get_updated_scores"),
    url(r'^create/sport/$', views.SportFormView.as_view(), name="create_sport")
]

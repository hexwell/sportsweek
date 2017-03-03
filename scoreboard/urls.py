from django.conf.urls import url

from . import views

app_name = 'scoreboard'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<sport_id>[0-9]+)/$', views.ranking_view, name='ranking')
]

from django.conf.urls import url

from . import views

app_name = 'scoreboard'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<sport_name>\w+)$', views.ranking_view, name='ranking')
]

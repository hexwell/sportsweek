import datetime

from django.db import models
from django.utils import timezone


class Sport(models.Model):
	name = models.CharField(max_length=20)

	def __str__(self):
		return self.name


class Team(models.Model):
	sport = models.ForeignKey(Sport, on_delete=models.CASCADE)
	name = models.CharField(max_length=20)
	score = models.IntegerField(default=0)

	def __str__(self):
		return self.name


class Event(models.Model):
	sport = models.ForeignKey(Sport, on_delete=models.CASCADE)
	team0 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='fk_team0')
	team1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='fk_team1')
	match_date = models.DateTimeField('match date')
	expired = False

	def is_imminent(self, interval):
		now = timezone.now()
		delta = self.match_date - now
		if delta <= datetime.timedelta():
			delta = now - self.match_date
			return delta <= datetime.timedelta(hours=3)
		return delta <= interval

	def __str__(self):
		return self.team0.name + ' VS ' + self.team1.name

import datetime

from django.db import models
from django.utils import timezone

show_for = datetime.timedelta(hours=3)
datetime_delta_zero = datetime.timedelta()


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
	team0 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team0')
	team1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team1')
	score0 = models.IntegerField(default=0)
	score1 = models.IntegerField(default=0)
	match_date = models.DateTimeField('match date')
	expired = False

	def is_imminent(self, interval):
		delta = self.__get_delta()
		return datetime_delta_zero <= delta <= interval

	def is_happening(self):
		delta = self.__get_delta()
		if delta <= datetime_delta_zero and not self.expired:
			delta = abs(delta)
			return delta <= show_for
		return False

	def is_past(self):
		delta = self.__get_delta()
		return delta <= datetime_delta_zero and not self.is_happening()

	def is_future(self, interval):
		delta = self.__get_delta()
		return delta >= interval

	def can_be_shown(self, interval):
		return self.is_happening() or self.is_imminent(interval)

	def __get_delta(self):
		return self.match_date - timezone.now()

	def __str__(self):
		return self.team0.name + ' VS ' + self.team1.name

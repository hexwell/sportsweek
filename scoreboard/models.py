from django.db import models


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
	match_date = models.DateTimeField('match date')
	team0 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='fk_team0')
	team1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='fk_team1')

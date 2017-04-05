from django.contrib import admin

from .models import Sport, Team, Event


class TeamInline(admin.TabularInline):
	model = Team
	extra = 1


class EventInline(admin.TabularInline):
	model = Event
	extra = 1

	def formfield_for_foreignkey(self, db_field, request, **kwargs):
		if request.resolver_match.args:
			current_sport = Sport.objects.filter(id=request.resolver_match.args[0])
		else:
			current_sport = None
		if db_field.name == "team0":
			kwargs["queryset"] = Team.objects.filter(sport=current_sport)
		if db_field.name == "team1":
			kwargs["queryset"] = Team.objects.filter(sport=current_sport)
		return super(EventInline, self).formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Sport)
class SportAdmin(admin.ModelAdmin):
	fields = ['name', 'creator']
	inlines = [TeamInline, EventInline]
	list_display = ('name', 'count_teams', 'count_events')
	search_fields = ['name', 'team__name']

	def count_teams(self, sport):
		return sport.team_set.count()

	def count_events(self, sport):
		return sport.event_set.count()

	count_teams.short_description = "Squadre"
	count_events.short_description = "Partite"

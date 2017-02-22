from django.shortcuts import render, loader
from django.http import HttpResponse


def index(request):
	template = loader.get_template('index.html')
	context = {'logged_in': False}
	return HttpResponse(template.render(context, request))

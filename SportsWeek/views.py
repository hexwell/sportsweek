from django.shortcuts import render


def index(request):
	context = {'username': request.user.username if request.user else None}
	return render(request, 'index.html', context)

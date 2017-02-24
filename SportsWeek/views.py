from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse


def index(request):
	return render(request, 'index.html')


def login_view(request):
	context = {
		'from': request.GET.get('from', reverse('index')),
		'wrong_login': request.GET.get('wrong_login', False)
	}
	return render(request, 'login.html', context)


def login_handler(request):
	username = request.POST['username']
	password = request.POST['password']
	user = authenticate(username=username, password=password)
	if user is not None:
		login(request, user)
		return HttpResponseRedirect(request.GET.get('from'))
	else:
		return HttpResponseRedirect(reverse('login') + '?from=' + request.GET.get('from') + ';wrong_login=True;')


def logout_handler(request):
	logout(request)
	return HttpResponseRedirect(request.GET.get('from'))

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterUserForm
from events.models import AppUser


def login_user(request):
	if request.method == "POST":
		username = request.POST["username"]
		password = request.POST["password"]
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect('home')
		else:
			messages.error(request, ("A intervenit o problema, incearca din nou..."))
			return redirect('login')
	else:
		return render(request, 'authenticate/login.html', {})


def logout_user(request):
	logout(request)
	messages.success(request, ("Te-ai deconectat cu success!"))
	return redirect('home')


def register_user(request):
	if request.method == "POST":
		form = RegisterUserForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username = username, password = password)
			login(request, user)
			messages.success(request, ("Cont inregistrat cu succes!"))
			
			new_Appuser = AppUser.objects.create(user=user)
			
			return redirect('home')

	else:
		form = RegisterUserForm()

	return render(request, 'authenticate/register_user.html', {
		'form':form,
		})
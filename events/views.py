from django.shortcuts import render, redirect
from django.core.files import File
from io import BytesIO
from django.core.files.base import ContentFile
from calendar import HTMLCalendar
from datetime import datetime, timedelta
from .models import Event, Ticket, Friendship, FriendRequest, AppUser
from .forms import TicketForm, EventForm
from django.http import HttpResponseRedirect
from itertools import chain
from sklearn.linear_model import LinearRegression
from django.contrib.auth.models import User
from django.contrib import messages
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error



def delete_event(request, event_id):

	event = Event.objects.get(pk=event_id)
	event.delete()
	messages.success(request, "Ai sters cu succes evenimentul " + event.name + "." )

	return redirect('list-events-organiser')


def update_event(request, event_id):

	appUser = initializare_user(request)

	event=Event.objects.get(pk=event_id)
	form = EventForm(request.POST or None, request.FILES or None, instance=event)
	if form.is_valid():
		
		event_hour = request.POST.get('hour','')
		my_user = request.user
		event = form.save(commit=False)
		event.organiser = my_user

		new_time_str = event_hour
		new_time = datetime.strptime(new_time_str, "%H:%M").time()
		event.eveniment_date = event.eveniment_date.replace(hour=new_time.hour, minute=new_time.minute)

		form.save()

		messages.success(request, "Ai actualizat cu succes evenimentul " + event.name + "." )
		return redirect('list-events-organiser')

	return render(request, 
			'events/update_eveniment.html', {
			'appUser':appUser,
			'eveniment':event,
			'form':form
				})


def initializare_user(request):

	appUser = None
	if request.user.is_authenticated:
		my_user = request.user
		appUser = AppUser.objects.get(user=my_user)
	return appUser


def add_event(request):

	appUser = initializare_user(request)

	submitted = False
	if request.method == "POST":
		form = EventForm(request.POST, request.FILES)
		if form.is_valid():

			event_hour = request.POST.get('hour','')

			my_user = request.user
			event = form.save(commit=False)
			event.organiser = my_user
			create_date = datetime.now()
			event.eveniment_create_date = create_date

			new_time_str = event_hour
			new_time = datetime.strptime(new_time_str, "%H:%M").time()

			if event.eveniment_date is None:
				messages.error(request, 'Trebuie sa completezi data evenimentului!')
				return redirect('add-event')

			event.eveniment_date = event.eveniment_date.replace(hour=new_time.hour, minute=new_time.minute)
			event.initial_tickets=event.tickets
			event.save()

			return HttpResponseRedirect('/add_event?submitted=True')
	else:
		form = EventForm
		if 'submitted' in request.GET:
			submitted = True
	return render(request, 
		'events/add_eveniment.html', {
		'appUser':appUser,
		'form':form,
		'submitted':submitted
		})


def add_funds(request):

	if request.user.is_authenticated:
		my_user = request.user
		appUser = AppUser.objects.get(user=my_user)

		if request.method == 'POST':
			funds_requested = request.POST.get('funds','')

			if funds_requested.isdigit() is False:
				messages.error(request, "Trebuie sa introduci suma pe care doresti sa o achizitionezi. Poti introduce doar un numar." )
				return redirect('add-funds')

			print(funds_requested)
			if request.user.is_authenticated:
				
				funds = appUser.funds
				funds = funds + int(funds_requested)
				appUser.funds=funds
				appUser.save()
				messages.success(request, "Ai cumparat cu succes fonduri in valoare de " + funds_requested + " RON." )

	return render(request, 
		'events/add_funds.html', {
		'appUser':appUser
		})


def make_ticket_gift_select_friend(request, ticket_id, friend_id):

	ticket = Ticket.objects.get(pk=ticket_id)
	friend = User.objects.get(pk=friend_id)

	ticket.user=friend
	ticket.is_gift=True
	ticket.save()

	messages.success(request, "Ai daruit un bilet catre: " + friend.username)
	return redirect('my-tickets')
	


	


def make_ticket_gift(request, ticket_id):

	appUser = initializare_user(request)
	ticket = Ticket.objects.get(pk=ticket_id)

	if request.user.is_authenticated:

		my_user = request.user

		friends_list1=Friendship.objects.filter(user1=my_user)

		lista1_aux=[]
		for fr in friends_list1:
			lista1_aux.append(User.objects.get(username=fr.user2))

		friends_list2=Friendship.objects.filter(user2=my_user)

		lista2_aux=[]
		for fr in friends_list2:
			lista2_aux.append(User.objects.get(username=fr.user1))

		friends_list=chain(lista1_aux, lista2_aux)

	return render(request, 
		'events/make_ticket_gift.html', {
		'appUser':appUser,
		'friends_list': friends_list,
		'ticket': ticket,
		'ticket_id':ticket_id
		})



def remove_friendrequest(request, user_id):
	
	user = request.user

	pending_user = User.objects.get(pk=user_id)
	friend_request = FriendRequest.objects.get(user1=user,user2=pending_user)

	messages.info(request, 'Cererea a fost stearsa.')
	friend_request.delete()
	return redirect('my-friends')





def remove_friend(request, friend_id):
	user = request.user
	ex_friend=User.objects.get(pk=friend_id)

	try:
		friendship=Friendship.objects.get(user1=user,user2=ex_friend)
	except Friendship.DoesNotExist:
		friendship=None

	if friendship is None:
		friendship=Friendship.objects.get(user1=ex_friend,user2=user)

	friendship.delete()
	return redirect('my-friends')




def decline_friendrequest(request, friendrequest_id):
	friend_requst=FriendRequest.objects.get(pk=friendrequest_id)	
	messages.info(request, 'Cererea a fost respinsa.')
	friend_requst.delete()
	return redirect('my-friends')




def accept_friendrequest(request, friendrequest_id):
	friend_requst=FriendRequest.objects.get(pk=friendrequest_id)
	messages.info(request, 'S-a acceptat cererea.')
	user1 = friend_requst.user1
	user2 = friend_requst.user2
	prietenie = Friendship.objects.create(user1=user1, user2=user2)
	prietenie.save()
	friend_requst.delete()
	return redirect('my-friends')





def search_user(request):
	if request.method=="POST":
		searched = request.POST['searched']
		if request.user.is_authenticated:
			user1 = request.user


		if searched == '':
			messages.error(request, 'Completeaza username-ul!')
			return redirect('my-friends')

		try:
			user2 = User.objects.get(username=searched)
		except User.DoesNotExist:
			messages.error(request, 'User-ul caruia incerci sa ii trimiti cerere nu exista!')
			return redirect('my-friends')



		if user1 == user2:
			messages.error(request, 'Nu poti sa iti trimiti tie o cerere de prietenie!')
			return redirect('my-friends')



		try:
			friendship=Friendship.objects.get(user1=user1,user2=user2)
		except Friendship.DoesNotExist:
			friendship=None
		if friendship is None:
			try:
				friendship=Friendship.objects.get(user1=user2,user2=user1)
			except Friendship.DoesNotExist:
				friendship=None
		if friendship is not None:
			messages.info(request, 'Deja esti prieten cu ' + searched + '!')
			return redirect('my-friends')




		try:
			check_if_friend_request_exist=FriendRequest.objects.get(user1=user1,user2=user2)
		except FriendRequest.DoesNotExist:
			check_if_friend_request_exist=None
		if check_if_friend_request_exist is None:
			try:
				check_if_friend_request_exist=FriendRequest.objects.get(user1=user2,user2=user1)
			except FriendRequest.DoesNotExist:
				check_if_friend_request_exist=None
		if check_if_friend_request_exist is not None:
			messages.info(request, 'Deja exista o cerere de prietenie activa intre tine si ' + searched + '!')
			return redirect('my-friends')



		messages.info(request, 'S-a trimis cererea de prietenie catre ' + user2.username + '.')
		friend_requst = FriendRequest.objects.create(user1=user1, user2=user2)
		friend_requst.save()
		return redirect('my-friends')


	
	else:
		return render(request, 
		'events/my_friends.html', {
	
			})

def all_events_organiser(request):
	appUser = initializare_user(request)

	

	if appUser is not None:
		evenimente_list_organiser=Event.objects.filter(organiser=appUser.user)
		return render(request, 
			'events/evenimente_list_organiser.html', {
			'appUser':appUser,
			'evenimente_list_organiser': evenimente_list_organiser
			})
	else:
		return render(request, 
			'events/evenimente_list_organiser.html', {
			
			})

def all_events(request):
	appUser = initializare_user(request)

	events_list=Event.objects.all()
	return render(request, 
		'events/evenimente_list.html', {
		'appUser':appUser,
		'evenimente_list': events_list
		})


def search_events(request):
	appUser = initializare_user(request)

	if request.method=="POST":
		searched = request.POST['searched']
		evenimente_gasite = Event.objects.filter(name__contains=searched)

		return render(request, 
		'events/search_evenimente.html', {
		'appUser':appUser,
		'searched':searched,
		'evenimente_gasite':evenimente_gasite
			})
	else:
		return render(request, 
		'events/search_evenimente.html', {
		'appUser':appUser
			})


def predict_sales(request, eveniment_id):
	eveniment = Event.objects.get(pk=eveniment_id)
	event_initial_tickets = int(eveniment.initial_tickets)
	event_create_date = eveniment.eveniment_create_date
	event_date = eveniment.eveniment_date.date()
	event_ticket_price = eveniment.ticket_price

	event_create_date = event_create_date.date()

	days=[]
	sold_tickets=[]
	today = datetime.now().date()
	
	
	#
	#ATENTTIE AICI pentru testare
	#

	#days_between_eventDate_today = int((today - event_create_date).total_seconds() / 86400 + 1)
	#5 zile de exemplu (testam)
	#setam evenimentul peste 10
	#modific in django admin

	days_between_eventDate_today = 5


	today = event_create_date

	for i in range(1, days_between_eventDate_today + 1):
		sold_tickets_today = 0
		print(today)
		try:
			bilete=Ticket.objects.filter(sale_date=today, eveniment=eveniment)
			print("bilete")
			print(len(bilete))
		except Ticket.DoesNotExist:
			bilete=None
		if bilete is None:
			sold_tickets_today = 0
		else:
			sold_tickets_today = len(bilete)
		if today.weekday() >= 4:
			is_long_weekend_day = 1
		else:
			is_long_weekend_day = 0
		days.append([i, is_long_weekend_day])
		if len(sold_tickets)==0:
			sold_tickets.append([int(sold_tickets_today)])
		else:
			sold_tickets.append([int(sold_tickets[-1][0])+int(sold_tickets_today)])
		today = today + timedelta(days=1)

	#testing
	#days = [[1,0],[2,0],[3,1],[4,1],[5,1]]
	#sold_tickets = [[8],[12],[17],[18],[24]]

	#inputs =[[1], [2], [3], [4], [5], [6], [7], [8], [9], [10], [11], [12], [13], [14], [15], [16], [17], [18], [19], [20], [21], [22], [23], [24], [25], [26], [27], [28], [29], [30], [31], [32]]
	#outputs = [[8], [12], [17], [18], [24], [29], [30], [30], [35], [39], [42], [45], [49], [52], [55], [58], [62], [65], [68], [72], [75], [78], [82], [85], [88], [92], [95], [98], [101], [105], [108], [111]]

	print("print de test")
	print(days)
	print(sold_tickets)
	predict_report(request, event_create_date, event_date, days, sold_tickets, event_initial_tickets, event_ticket_price, eveniment_id)
	print("s-a prezis")


def show_eveniment(request, eveniment_id):
	appUser = initializare_user(request)

	submitted = False
	eveniment = Event.objects.get(pk=eveniment_id)
	if request.method == "POST":
		form = TicketForm(request.POST)
		if form.is_valid():
			number_of_tickets = form.cleaned_data['number_of_tickets']

			if int(number_of_tickets) > int(eveniment.tickets):
				messages.error(request, 'Mai sunt disponibile doar ' + eveniment.tickets + ' bilete la acest eveniment.')
				return redirect('list-evenimente')

			price_of_tickets = int(number_of_tickets) * int(eveniment.ticket_price)
			appUser = AppUser.objects.get(user=request.user)

			if price_of_tickets > appUser.funds:
				messages.error(request, 'Fonduri insuficiente!')
				return redirect('add-funds')


			nume = form.cleaned_data['nume']
			prenume = form.cleaned_data['prenume']
			bilet = form.save(commit=False)
			my_user = request.user
			bilet.user = my_user
			bilet.eveniment = eveniment

			sale_date = datetime.now()
			sale_date = sale_date.date()
			bilet.sale_date = sale_date

			bilet.save()
			for i in range(int(number_of_tickets)-1):
				bilet=Ticket(nume=nume, prenume=prenume, user=my_user, eveniment=eveniment, sale_date = sale_date)
				bilet.save()

			remaining_tickets=int(eveniment.tickets)-int(number_of_tickets)
			eveniment.tickets=str(remaining_tickets)
			eveniment.save()

			appUser.funds = appUser.funds - price_of_tickets
			appUser.save()

			if remaining_tickets <= int(eveniment.initial_tickets)/2:
				if eveniment.predicted == False:
					predict_sales(request, eveniment_id)


			if int(number_of_tickets) == 1:
				messages.success(request, 'Ai cumpara cu succes un bilet la evenimentul ' + eveniment.name + '.')
			else:
				messages.success(request, 'Ai cumpara cu succes ' + number_of_tickets + ' bilete la evenimentul ' + eveniment.name + '.')
			return redirect('my-tickets')
		
			
			
	else:
		form = TicketForm
		if 'submitted' in request.GET:
			submitted = True
	return render(request, 
		'events/show_eveniment.html', {
		'appUser':appUser,
		'form':form,
		'submitted':submitted,
		'eveniment':eveniment
		})


def my_tickets(request):
	appUser = initializare_user(request)

	if request.user.is_authenticated:
		my_user = request.user
		bilete_list=Ticket.objects.filter(user=my_user)

		return render(request, 
		'events/my_tickets.html', {
		'appUser':appUser,
		'bilete_list': bilete_list
		})
	else:
		return render(request, 
		'events/my_tickets.html', {
		'appUser':appUser
		})

def my_friends(request):
	appUser = initializare_user(request)

	if request.user.is_authenticated:
		my_user = request.user
		friends_list1=Friendship.objects.filter(user1=my_user)

		lista1=[]
		for fr in friends_list1:
			lista1.append(User.objects.get(username=fr.user2))


		friends_list2=Friendship.objects.filter(user2=my_user)

		lista2=[]
		for fr in friends_list2:
			lista2.append(User.objects.get(username=fr.user1))


		#friends_list=chain(friends_list1,friends_list2)
		friends_list=chain(lista1,lista2)


		friend_request_list=FriendRequest.objects.filter(user2=my_user)



		friend_requst_pending = FriendRequest.objects.filter(user1=my_user)
		pending_list = []
		for p in friend_requst_pending:
			pending_list.append(User.objects.get(username=p.user2))





		return render(request, 
		'events/my_friends.html', {
		'appUser':appUser,
		'friends_list': friends_list,
		'friend_request_list':friend_request_list,
		'pending_list': pending_list
		})
	else:
		return render(request, 
		'events/my_friends.html', {
		appUser:appUser
		})



def home(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
	appUser = None
	if request.user.is_authenticated:
		my_user = request.user
		appUser = AppUser.objects.get(user=my_user)

	return render(request, 
		'events/home.html', {
		"appUser": appUser,
		})


def predict_report(request, event_create_date, event_date, days, sold_tickets, event_initial_tickets, ticket_price, event_id):
	days_between_createDate_eventDate = int((event_date - event_create_date).total_seconds() / 86400 + 1)
	days_train, days_test, sold_tickets_train, sold_tickets_test = train_test_split(days, sold_tickets, test_size=0.3)
	regresor = LinearRegression()
	regresor.fit(days_train, sold_tickets_train)

	days_train = sorted(days_train, key=lambda x: x[0])
	sold_tickets_train = sorted(sold_tickets_train, key=lambda x: x[0])
	days_test = sorted(days_test, key=lambda x: x[0])
	sold_tickets_test = sorted(sold_tickets_test, key=lambda x: x[0])
	last_day = len(days_train) + len(days_test)
	today = event_create_date + timedelta(days=last_day-1)
	remainings_days = days_between_createDate_eventDate - last_day

	for i in range(remainings_days):
		today = today + timedelta(days=1)
		if today.weekday() >= 4:
			is_long_weekend_day = 1
		else:
			is_long_weekend_day = 0
		days_train.append([last_day + 1 + i, is_long_weekend_day])
		predicted_sales = regresor.predict([days_train[-1]])
		sold_tickets_train.append([int(predicted_sales)])

	#"raportul" predictiei
	report = ''
	#vedem cate bilete s-au vandut in total
	all_sold_tickets = sold_tickets_train[-1][0]
	balance_of_tickets = event_initial_tickets - all_sold_tickets

	if balance_of_tickets < 0:
		days_without_tickets = 0
		for sold_tickets_per_day in reversed(sold_tickets_train):
			if int(sold_tickets_per_day[0]) > event_initial_tickets:
				days_without_tickets = days_without_tickets + 1
		days_with_tickets = days_between_createDate_eventDate - days_without_tickets
		report = report + "Sold out! Conform predictiei noastre pe baza celor " + str(int(event_initial_tickets/2)) + " bilete vandute deja (jumatate din numarul de bilete initiale) si tinand cont de posibilele zile in care se fac mai multe vanzari (vineri, sambata, duminica), pana la data evenimentului, " + str(event_date) + ", s-ar vinde " + str(all_sold_tickets) + " de bilete, adica cu " + str(balance_of_tickets * (-1)) + " mai multe bilete decat sunt disponibile. "
		report = report + "In ziua cu numarul " + str(days_with_tickets + 1) + " (" + str(event_create_date + timedelta(days=days_with_tickets)) + "), veti ramane fara bilete la evenimentul dumneavoastra. In aceasta zi, vanzarile ar fi ajuns la "+ str(int(sold_tickets_train[days_with_tickets-len(days_test)][0]) - event_initial_tickets) + " bilet/bilete peste numarul de bilete disponibile pentru acest eveniment."
	else:
		report = report + "Ne pare rau! Conform predictiei noastre e posibil ca evenimentul dumneavoastra sa nu fie sold out. Pana la data evenimentului, " + str(event_date) + ", este posibil sa ramaneti in stoc cu " + str(balance_of_tickets) + " bilete nevandute. Aceasta predictie a fost generata automat dupa vanzarea a " + str(int(event_initial_tickets/2)) + " bilete, adica jumatate din numarul initial de bilete disponibile. Am tinut cont si de faptul ca in zilele de vineri, sambata si duminica s-ar putea face mai multe vanzari."
		report = report + "Va recomandam sa aprofundati sau sa aplicati o strategie diferita de marketing. De asemenea, ati putea aplica o reducere de 10% pentru pretul biletelor la evenimentul dumneavoastra, actualizandu-l la " + str(ticket_price * 90 / 100) + " RON."

	predicted_sales_test = regresor.predict(days_test)
	mse = mean_squared_error(sold_tickets_test, predicted_sales_test)
	print(mse)

	zile_train= [ziua[0] for ziua in days_train]
	bilete_vandute_train = [bilete[0] for bilete in sold_tickets_train]

	plt.plot(zile_train, bilete_vandute_train, marker = 'o', color='green')
	plt.xlabel('Ziua')
	plt.ylabel('Numarul de bilete vandute in total pana la ziua respectiva')
	plt.title('Vanzari bilete pe zi')
	buffer = BytesIO()
	plt.savefig(buffer, format='png')
	buffer.seek(0)
	image_file = ContentFile(buffer.getvalue(), name='plot.png')
	eveniment=Event.objects.get(pk=event_id)
	eveniment.prediction_image = image_file
	eveniment.predicted = True
	eveniment.prediction_text = report
	eveniment.save()

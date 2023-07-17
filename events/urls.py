"""
URL configuration for events_website project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

urlpatterns = [
    path('events', views.all_events, name="list-events"),
    path('events_organiser', views.all_events_organiser, name="list-events-organiser"),
    path('delete_event/<event_id>', views.delete_event, name="delete-event"),
    path('update_event/<event_id>', views.update_event, name="update-event"),
    path('search_events', views.search_events, name="search-events"),
    path('show_eveniment/<eveniment_id>', views.show_eveniment, name="show-eveniment"),
    path('my_tickets', views.my_tickets, name="my-tickets"),
    path('my_friends', views.my_friends, name="my-friends"),
    path('search_user', views.search_user, name="search-user"),
    path('accept_friendrequest/<friendrequest_id>', views.accept_friendrequest, name="accept-friendrequest"),
    path('decline_friendrequest/<friendrequest_id>', views.decline_friendrequest, name="decline-friendrequest"),
    path('remove_friend/<friend_id>/', views.remove_friend, name="remove-friend"),
    path('remove_friendrequest/<user_id>/', views.remove_friendrequest, name="remove-friendrequest"),
    path('make_ticket_gift/<ticket_id>/', views.make_ticket_gift, name="make-ticket-gift"),
    path('make_ticket_gift_select_friend/<ticket_id>/<friend_id>', views.make_ticket_gift_select_friend, name="make-ticket-gift-select-friend"),
    path('add_funds', views.add_funds, name="add-funds"),
    path('add_event', views.add_event, name="add-event"),
    path('', views.home, name="home"),
    path('<int:year>/<str:month>/', views.home, name="home"),

]

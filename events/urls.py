from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    #int: numbers
    #str: strings
    #path: urls
    #slug: hyphen-and_underscore_stuff
    #UUID: universaly unique identifier

     path('<int:year>/<str:month>/', views.home, name='home'),
     path('events' , views.all_events, name='list-events'),
     path('add_venue' , views.add_venue, name= 'add-venue'),
     path('venue' , views.list_venues, name='list-venues'),
     path('show_venue/<venue_id>' , views.show_venue, name='show-venue'),
     path('search_venues' , views.search_venues, name='search-venues'),
     path('update_venues/<venue_id>' , views.update_venues, name='update-venues'),
     path('update_event/<event_id>' , views.update_event, name='update-event'),
     path('add_event' , views.add_event, name= 'add-event'),
     path('delete_event/<event_id>' , views.delete_event, name= 'delete-event'),
     path('delete_venue/<venue_id>' , views.delete_venue, name= 'delete-venue'),
     path('venue_text' , views.venue_text, name= 'venue-text'),
     path('venue_csv' , views.venue_csv, name= 'venue-csv'),
     path('venue_pdf' , views.venue_pdf, name= 'venue-pdf'),
   
]

from django.shortcuts import redirect, render
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from django.http import HttpResponseRedirect
from .models import Event
from. forms import VenueForm , EventForm
from . models import Venue
from django.http import HttpResponse
import csv

from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter


# Import Pagination Stuff
from django.core.paginator import Paginator




# Generate a PDF File Venue List

def venue_pdf(request):

    # Create Bytesttream buffer
    buf = io.BytesIO()

    # Create Canvas
    c = canvas.Canvas(buf, pagesize=letter , bottomup=0)

    # Create a text Object
    textob = c.beginText()
    textob.setTextOrigin(inch , inch)
    textob.setFont("Helvetica" , 14)

    # Add some lines of Text
    #lines = ["Line 1", "Line 2" , "Line 3"]

    # Designate the Model
    venues = Venue.objects.all()

    # Create blank list
    lines = []

    # Loop

    for venue in venues:
        lines.append(venue.name)
        lines.append(venue.address)
        lines.append(venue.zip_code)
        lines.append(venue.phone)
        lines.append(venue.web)
        lines.append(venue.email_address)
        lines.append(" ")


    # Loop

    for line in lines:
        textob.textLine(line)

    # Finish Up
    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename='venue.pdf')
    
# <--------------------------------------------------------------------------------------------------------------------------------> #

#-------------------------------#
# Generate Text File Venue List #
#-------------------------------#

def venue_csv(request):

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=venues.csv'


    # Create CSV Writer

    writer = csv.writer(response)

    # Designate the Models

    venues = Venue.objects.all()


    # Add Collunm Heading to CSV File

    writer.writerow(['Venue Name' , 'Address' , 'Zip Code' , 'Phone' , 'Web Address' , 'E-mail'])


    # Loop Through and Output

    for venue in venues:

       writer.writerow([venue.name , venue.address , venue.zip_code , venue.phone , venue.web , venue.email_address])
       
    return response




def venue_text(request):

    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=venues.txt'


    # Designate the Models

    venues = Venue.objects.all()

    # Create Blank List

    lines = []

    # Loop Through and Output

    for venue in venues:

        lines.append(f'{venue.name}\n{venue.address}{venue.zip_code}\n{venue.phone}\n{venue.web}\n{venue.email_address}\n\n\n\n')

    #lines = ["This is line 1 \n",
    #"This is Line 2 \n",
    #"This is Line 3 \n",
    #"Diego is Awsome!!!! \n"]

    # Write to Text File

    response.writelines(lines)
    return response




# Create your views here.

def delete_venue(request , venue_id):

    venue = Venue.objects.get(pk=venue_id)
    venue.delete()

    return redirect('list-venues')




def delete_event(request , event_id):

    event = Event.objects.get(pk=event_id)
    event.delete()

    return redirect('list-events')



def update_event(request, event_id):

     event = Event.objects.get(pk=event_id)

     form = EventForm(request.POST or None ,  instance=event) # instance = venue -> Coloca os dados dentro dos campos para serem editados

     if form.is_valid():
         form.save()
         return redirect('list-events')

     return render(request, 'events/update_event.html' , {'event': event , 'form': form} )



def add_event(request):

    submitted = False
    if request.method == 'POST':

        form = EventForm(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/add_event?submitted=True')

    else:
        form = EventForm

        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'events/add_event.html' , {'form': form , 'submitted': submitted} )



def update_venues(request, venue_id):

     venue = Venue.objects.get(pk=venue_id)

     form =  form = VenueForm(request.POST or None ,  instance=venue) # instance = venue -> Coloca os dados dentro dos campos para serem editados

     if form.is_valid():
         form.save()
         return redirect('list-venues')

     return render(request, 'events/update_venue.html' , {'venue': venue , 'form': form} )




def search_venues(request):

    if request.method == "POST":

        searched = request.POST['searched']

        venues = Venue.objects.filter(name__contains=searched)

        return render(request, 'events/search_venues.html' , {'searched': searched , 'venues': venues} )

    else:

        return render(request, 'events/search_venues.html' , {} )    


def show_venue(request, venue_id):

    venue = Venue.objects.get(pk=venue_id)

    return render(request, 'events/show_venue.html' , {'venue': venue } )


#-------------------------------#
#-------List the Venues---------#
#-------------------------------#

def list_venues(request):

    #venue_list = Venue.objects.all().order_by('name') # Order by Name - order_by('?') means randomly

    venue_list = Venue.objects.all()

    # Set up Pagination
    p = Paginator(Venue.objects.all(), 2)
    page = request.GET.get('page')
    venues = p.get_page(page)
    nums = "a" * venues.paginator.num_pages

    return render(request, 'events/venue.html' , {'venue_list': venue_list , 'venues': venues, 'nums': nums})


def add_venue(request):

    submitted = False
    if request.method == 'POST':

        form = VenueForm(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/add_venue?submitted=True')

    else:
        form = VenueForm

        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'events/add_venue.html' , {'form': form , 'submitted': submitted} )




def all_events(request):

    event_list = Event.objects.all().order_by('event_date') # ('-name') -> Ordem Contrária

    return render(request, 'events/event_list.html' , {'event_list': event_list} )



def home(request, year=datetime.now().year, month=datetime.now().strftime('%B')):

    name = "Jonh"
    month = month.title() # Captalize the First Letter
    #month = month.capitalize() # Captalize the First Letter (second option)

    #Convert month from name to number

    month_number = list(calendar.month_name).index(month)
    month_number = int(month_number)

    # Create a Caldendar

    cal = HTMLCalendar().formatmonth(year, month_number)

    # Get the current Year

    now = datetime.now()
    current_year = now.year

    # Get curretn time

    time = now.strftime('%I:%M:%S %p') # %I - 12:00 %H 24:00

    return render(request, 'events/home.html', {'name':name , 'year':year , 'month':month, 'month_number':month_number, 'cal':cal, 'current_year':current_year, 'time': time} )

